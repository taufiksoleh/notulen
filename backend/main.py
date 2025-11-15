"""
Notulen - Indonesian Meeting Note Taker
FastAPI backend for speech-to-text processing
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import tempfile
import logging
from datetime import datetime

from services.transcription import TranscriptionService
from services.llm_processor import LLMProcessor
from models.database import Database, Meeting

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notulen API",
    description="Indonesian Meeting Note Taker with hybrid STT processing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
transcription_service = TranscriptionService()
llm_processor = LLMProcessor()
db = Database()


class TranscriptionRequest(BaseModel):
    language: Optional[str] = "auto"
    model_preference: Optional[str] = "auto"  # auto, whisper, wav2vec


class TranscriptionResponse(BaseModel):
    id: str
    text: str
    language: str
    model_used: str
    segments: Optional[List[dict]] = None
    duration: float
    created_at: str


class SummaryRequest(BaseModel):
    meeting_id: str


class SummaryResponse(BaseModel):
    meeting_id: str
    summary: str
    action_items: List[str]
    key_points: List[str]
    participants: Optional[List[str]] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Notulen API",
        "status": "running",
        "version": "1.0.0",
        "models": {
            "whisper": transcription_service.whisper_available,
            "wav2vec": transcription_service.wav2vec_available
        }
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "whisper": "available" if transcription_service.whisper_available else "unavailable",
            "wav2vec": "available" if transcription_service.wav2vec_available else "unavailable",
            "llm": "available" if llm_processor.is_available() else "unavailable"
        }
    }


@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = "auto",
    model_preference: str = "auto"
):
    """
    Transcribe audio file to text

    Args:
        file: Audio file (mp3, wav, m4a, etc.)
        language: Language code (auto, id, en) - auto will detect
        model_preference: Which model to use (auto, whisper, wav2vec)
    """
    try:
        logger.info(f"Received transcription request: {file.filename}, language={language}, model={model_preference}")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Perform transcription
            result = await transcription_service.transcribe(
                audio_path=tmp_path,
                language=language,
                model_preference=model_preference
            )

            # Save to database
            meeting = db.create_meeting(
                title=f"Meeting - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                audio_filename=file.filename,
                transcription=result["text"],
                language=result["language"],
                model_used=result["model_used"],
                segments=result.get("segments"),
                duration=result.get("duration", 0)
            )

            logger.info(f"Transcription completed: meeting_id={meeting.id}, model={result['model_used']}")

            return TranscriptionResponse(
                id=meeting.id,
                text=result["text"],
                language=result["language"],
                model_used=result["model_used"],
                segments=result.get("segments"),
                duration=result.get("duration", 0),
                created_at=meeting.created_at.isoformat()
            )

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@app.post("/api/summarize", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generate meeting summary and extract action items

    Args:
        request: Contains meeting_id to summarize
    """
    try:
        # Get meeting from database
        meeting = db.get_meeting(request.meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")

        logger.info(f"Generating summary for meeting: {meeting.id}")

        # Generate summary using LLM
        summary_data = await llm_processor.generate_summary(
            transcription=meeting.transcription,
            language=meeting.language
        )

        # Update meeting with summary
        db.update_meeting_summary(
            meeting_id=meeting.id,
            summary=summary_data["summary"],
            action_items=summary_data["action_items"],
            key_points=summary_data["key_points"]
        )

        logger.info(f"Summary generated for meeting: {meeting.id}")

        return SummaryResponse(
            meeting_id=meeting.id,
            summary=summary_data["summary"],
            action_items=summary_data["action_items"],
            key_points=summary_data["key_points"],
            participants=summary_data.get("participants")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")


@app.get("/api/meetings")
async def list_meetings(limit: int = 50, offset: int = 0):
    """List all meetings"""
    try:
        meetings = db.list_meetings(limit=limit, offset=offset)
        return {
            "meetings": [
                {
                    "id": m.id,
                    "title": m.title,
                    "created_at": m.created_at.isoformat(),
                    "duration": m.duration,
                    "language": m.language,
                    "has_summary": m.summary is not None
                }
                for m in meetings
            ],
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Failed to list meetings: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/meetings/{meeting_id}")
async def get_meeting(meeting_id: str):
    """Get full meeting details"""
    try:
        meeting = db.get_meeting(meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")

        return {
            "id": meeting.id,
            "title": meeting.title,
            "transcription": meeting.transcription,
            "summary": meeting.summary,
            "action_items": meeting.action_items,
            "key_points": meeting.key_points,
            "language": meeting.language,
            "model_used": meeting.model_used,
            "duration": meeting.duration,
            "created_at": meeting.created_at.isoformat(),
            "segments": meeting.segments
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get meeting: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/meetings/{meeting_id}")
async def delete_meeting(meeting_id: str):
    """Delete a meeting"""
    try:
        success = db.delete_meeting(meeting_id)
        if not success:
            raise HTTPException(status_code=404, detail="Meeting not found")

        return {"message": "Meeting deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete meeting: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
