from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func
from app.models import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    audio_file_path = Column(String(512), nullable=False)
    audio_duration = Column(Float, nullable=True)  # in seconds

    # Transcription
    transcription = Column(Text, nullable=True)
    transcription_segments = Column(JSON, nullable=True)  # Timestamped segments
    detected_language = Column(String(10), nullable=True)
    model_used = Column(String(100), nullable=True)  # whisper or wav2vec

    # LLM Processing
    summary = Column(Text, nullable=True)
    action_items = Column(JSON, nullable=True)  # List of action items
    key_points = Column(JSON, nullable=True)  # List of key discussion points

    # Status
    status = Column(String(50), default="uploaded")  # uploaded, processing, completed, failed
    error_message = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Meeting(id={self.id}, title='{self.title}', status='{self.status}')>"
