"""
Database models and operations
Uses SQLite for simplicity (can be upgraded to PostgreSQL)
"""

import os
import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Meeting:
    """Meeting data model"""
    id: str
    title: str
    audio_filename: str
    transcription: str
    language: str
    model_used: str
    duration: float
    created_at: datetime
    summary: Optional[str] = None
    action_items: Optional[List[str]] = None
    key_points: Optional[List[str]] = None
    segments: Optional[List[Dict]] = None


class Database:
    """Database manager for meetings"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.getenv("DATABASE_PATH", "data/notulen.db")

        self.db_path = db_path

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Initialize database
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS meetings (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    audio_filename TEXT,
                    transcription TEXT NOT NULL,
                    language TEXT,
                    model_used TEXT,
                    duration REAL,
                    summary TEXT,
                    action_items TEXT,
                    key_points TEXT,
                    segments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")

    def create_meeting(
        self,
        title: str,
        audio_filename: str,
        transcription: str,
        language: str,
        model_used: str,
        duration: float,
        segments: Optional[List[Dict]] = None
    ) -> Meeting:
        """Create a new meeting record"""

        meeting_id = str(uuid.uuid4())
        created_at = datetime.utcnow()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO meetings (
                    id, title, audio_filename, transcription, language,
                    model_used, duration, segments, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                meeting_id,
                title,
                audio_filename,
                transcription,
                language,
                model_used,
                duration,
                json.dumps(segments) if segments else None,
                created_at.isoformat()
            ))
            conn.commit()

        logger.info(f"Meeting created: {meeting_id}")

        return Meeting(
            id=meeting_id,
            title=title,
            audio_filename=audio_filename,
            transcription=transcription,
            language=language,
            model_used=model_used,
            duration=duration,
            created_at=created_at,
            segments=segments
        )

    def get_meeting(self, meeting_id: str) -> Optional[Meeting]:
        """Get meeting by ID"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM meetings WHERE id = ?",
                (meeting_id,)
            )
            row = cursor.fetchone()

        if not row:
            return None

        return Meeting(
            id=row["id"],
            title=row["title"],
            audio_filename=row["audio_filename"],
            transcription=row["transcription"],
            language=row["language"],
            model_used=row["model_used"],
            duration=row["duration"],
            summary=row["summary"],
            action_items=json.loads(row["action_items"]) if row["action_items"] else None,
            key_points=json.loads(row["key_points"]) if row["key_points"] else None,
            segments=json.loads(row["segments"]) if row["segments"] else None,
            created_at=datetime.fromisoformat(row["created_at"])
        )

    def list_meetings(self, limit: int = 50, offset: int = 0) -> List[Meeting]:
        """List meetings with pagination"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM meetings ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()

        meetings = []
        for row in rows:
            meetings.append(Meeting(
                id=row["id"],
                title=row["title"],
                audio_filename=row["audio_filename"],
                transcription=row["transcription"],
                language=row["language"],
                model_used=row["model_used"],
                duration=row["duration"],
                summary=row["summary"],
                action_items=json.loads(row["action_items"]) if row["action_items"] else None,
                key_points=json.loads(row["key_points"]) if row["key_points"] else None,
                segments=json.loads(row["segments"]) if row["segments"] else None,
                created_at=datetime.fromisoformat(row["created_at"])
            ))

        return meetings

    def update_meeting_summary(
        self,
        meeting_id: str,
        summary: str,
        action_items: List[str],
        key_points: List[str]
    ) -> bool:
        """Update meeting with summary and insights"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE meetings
                SET summary = ?, action_items = ?, key_points = ?
                WHERE id = ?
            """, (
                summary,
                json.dumps(action_items),
                json.dumps(key_points),
                meeting_id
            ))
            conn.commit()

            return cursor.rowcount > 0

    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM meetings WHERE id = ?",
                (meeting_id,)
            )
            conn.commit()

            return cursor.rowcount > 0
