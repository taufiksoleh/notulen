from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class MeetingBase(BaseModel):
    title: str
    description: Optional[str] = None


class MeetingCreate(MeetingBase):
    pass


class MeetingResponse(MeetingBase):
    id: int
    audio_file_path: str
    audio_duration: Optional[float] = None
    transcription: Optional[str] = None
    transcription_segments: Optional[List[Dict[str, Any]]] = None
    detected_language: Optional[str] = None
    model_used: Optional[str] = None
    summary: Optional[str] = None
    action_items: Optional[List[str]] = None
    key_points: Optional[List[str]] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TranscriptionRequest(BaseModel):
    language: Optional[str] = "id"  # Default to Indonesian
    use_indonesian_model: bool = True


class TranscriptionResponse(BaseModel):
    text: str
    segments: Optional[List[Dict[str, Any]]] = None
    language: str
    model_used: str


class SummaryRequest(BaseModel):
    transcription: str
    language: str = "id"


class SummaryResponse(BaseModel):
    summary: str
    action_items: List[str]
    key_points: List[str]


class HealthResponse(BaseModel):
    status: str
    message: str
    models_loaded: Dict[str, bool]
