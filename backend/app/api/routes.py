from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from pathlib import Path
import logging
from datetime import datetime
import librosa

from app.models import get_db
from app.models.meeting import Meeting
from app.models.schemas import (
    MeetingResponse,
    MeetingCreate,
    TranscriptionResponse,
    SummaryResponse,
    HealthResponse
)
from app.services.stt_service import stt_service
from app.services.llm_service import llm_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    models_status = stt_service.get_models_status()
    return {
        "status": "healthy",
        "message": "Notulen API is running",
        "models_loaded": models_status
    }


@router.post("/meetings", response_model=MeetingResponse)
async def create_meeting(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form("id"),
    use_indonesian_model: bool = Form(True),
    db: Session = Depends(get_db)
):
    """
    Upload audio file and create a new meeting

    This endpoint:
    1. Uploads the audio file
    2. Transcribes it using STT models
    3. Generates summary and action items using LLM
    """
    try:
        # Validate file extension
        file_ext = Path(audio_file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not supported. Allowed types: {settings.ALLOWED_AUDIO_EXTENSIONS}"
            )

        # Create upload directory if it doesn't exist
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{audio_file.filename}"
        file_path = upload_dir / filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        logger.info(f"Audio file saved: {file_path}")

        # Get audio duration
        try:
            y, sr = librosa.load(str(file_path), sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
        except Exception as e:
            logger.warning(f"Failed to get audio duration: {e}")
            duration = None

        # Create meeting record
        meeting = Meeting(
            title=title,
            description=description,
            audio_file_path=str(file_path),
            audio_duration=duration,
            status="processing"
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)

        logger.info(f"Meeting created with ID: {meeting.id}")

        # Transcribe audio
        try:
            transcription_result = stt_service.transcribe(
                audio_path=str(file_path),
                language=language,
                use_indonesian_model=use_indonesian_model
            )

            meeting.transcription = transcription_result["text"]
            meeting.transcription_segments = transcription_result.get("segments")
            meeting.detected_language = transcription_result["language"]
            meeting.model_used = transcription_result["model_used"]

            logger.info(f"Transcription completed for meeting {meeting.id}")

            # Generate summary and action items using LLM
            if llm_service.is_available():
                try:
                    summary_result = llm_service.generate_summary(
                        transcription=meeting.transcription,
                        language=meeting.detected_language
                    )

                    meeting.summary = summary_result["summary"]
                    meeting.action_items = summary_result["action_items"]
                    meeting.key_points = summary_result["key_points"]

                    logger.info(f"Summary generated for meeting {meeting.id}")
                except Exception as e:
                    logger.error(f"Failed to generate summary: {e}")
                    # Continue without summary
            else:
                logger.warning("LLM service not available, skipping summary generation")

            meeting.status = "completed"
            meeting.processed_at = datetime.now()

        except Exception as e:
            logger.error(f"Processing failed for meeting {meeting.id}: {e}")
            meeting.status = "failed"
            meeting.error_message = str(e)

        db.commit()
        db.refresh(meeting)

        return meeting

    except Exception as e:
        logger.error(f"Failed to create meeting: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meetings", response_model=List[MeetingResponse])
async def list_meetings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all meetings"""
    meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).offset(skip).limit(limit).all()
    return meetings


@router.get("/meetings/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """Get a specific meeting by ID"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.delete("/meetings/{meeting_id}")
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    """Delete a meeting"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Delete audio file
    try:
        if os.path.exists(meeting.audio_file_path):
            os.remove(meeting.audio_file_path)
    except Exception as e:
        logger.warning(f"Failed to delete audio file: {e}")

    # Delete database record
    db.delete(meeting)
    db.commit()

    return {"message": "Meeting deleted successfully"}


@router.post("/meetings/{meeting_id}/regenerate-summary", response_model=MeetingResponse)
async def regenerate_summary(meeting_id: int, db: Session = Depends(get_db)):
    """Regenerate summary for a meeting"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if not meeting.transcription:
        raise HTTPException(status_code=400, detail="Meeting has no transcription")

    if not llm_service.is_available():
        raise HTTPException(status_code=503, detail="LLM service not available")

    try:
        summary_result = llm_service.generate_summary(
            transcription=meeting.transcription,
            language=meeting.detected_language or "id"
        )

        meeting.summary = summary_result["summary"]
        meeting.action_items = summary_result["action_items"]
        meeting.key_points = summary_result["key_points"]

        db.commit()
        db.refresh(meeting)

        return meeting

    except Exception as e:
        logger.error(f"Failed to regenerate summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
