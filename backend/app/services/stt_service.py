import whisper
import torch
import logging
from pathlib import Path
from typing import Dict, Optional, List
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class STTService:
    """
    Speech-to-Text Service supporting both Whisper and Indonesian Wav2vec 2.0
    """

    def __init__(self):
        self.whisper_model = None
        self.indonesian_model = None
        self.indonesian_processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"STT Service initialized on device: {self.device}")

    def load_whisper_model(self):
        """Load Whisper model"""
        if self.whisper_model is None:
            try:
                logger.info(f"Loading Whisper model: {settings.WHISPER_MODEL}")
                self.whisper_model = whisper.load_model(settings.WHISPER_MODEL, device=self.device)
                logger.info(f"Whisper model '{settings.WHISPER_MODEL}' loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                raise

    def load_indonesian_model(self):
        """Load Indonesian Wav2vec 2.0 model"""
        if self.indonesian_model is None and settings.USE_INDONESIAN_MODEL:
            try:
                logger.info(f"Loading Indonesian model: {settings.INDONESIAN_MODEL_NAME}")
                self.indonesian_processor = Wav2Vec2Processor.from_pretrained(
                    settings.INDONESIAN_MODEL_NAME
                )
                self.indonesian_model = Wav2Vec2ForCTC.from_pretrained(
                    settings.INDONESIAN_MODEL_NAME
                ).to(self.device)
                logger.info("Indonesian Wav2vec model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Indonesian model: {e}")
                # Don't raise - fall back to Whisper
                self.indonesian_model = None

    def detect_language(self, audio_path: str) -> str:
        """
        Detect language using Whisper's built-in language detection
        """
        try:
            if self.whisper_model is None:
                self.load_whisper_model()

            # Load audio
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)

            # Make log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.whisper_model.device)

            # Detect language
            _, probs = self.whisper_model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)

            logger.info(f"Detected language: {detected_lang} (confidence: {probs[detected_lang]:.2f})")
            return detected_lang
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return "id"  # Default to Indonesian

    def transcribe_with_indonesian_model(self, audio_path: str) -> Dict:
        """
        Transcribe audio using Indonesian Wav2vec 2.0 model
        """
        try:
            if self.indonesian_model is None:
                self.load_indonesian_model()

            if self.indonesian_model is None:
                raise Exception("Indonesian model not available")

            # Load and resample audio to 16kHz
            audio_array, sampling_rate = librosa.load(audio_path, sr=16000)

            # Process audio
            inputs = self.indonesian_processor(
                audio_array,
                sampling_rate=16000,
                return_tensors="pt",
                padding=True
            )

            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Perform inference
            with torch.no_grad():
                logits = self.indonesian_model(inputs.input_values).logits

            # Decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.indonesian_processor.batch_decode(predicted_ids)[0]

            return {
                "text": transcription,
                "segments": None,  # Wav2vec doesn't provide segments
                "language": "id",
                "model_used": "indonesian-wav2vec"
            }

        except Exception as e:
            logger.error(f"Indonesian model transcription failed: {e}")
            raise

    def transcribe_with_whisper(self, audio_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcribe audio using Whisper model
        """
        try:
            if self.whisper_model is None:
                self.load_whisper_model()

            logger.info(f"Transcribing with Whisper (language: {language or 'auto'})")

            # Transcribe
            result = self.whisper_model.transcribe(
                audio_path,
                language=language,
                verbose=False
            )

            # Format segments
            segments = []
            if "segments" in result:
                for seg in result["segments"]:
                    segments.append({
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": seg["text"].strip()
                    })

            return {
                "text": result["text"].strip(),
                "segments": segments,
                "language": result.get("language", language or "unknown"),
                "model_used": f"whisper-{settings.WHISPER_MODEL}"
            }

        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            raise

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        use_indonesian_model: bool = True
    ) -> Dict:
        """
        Smart transcription: automatically choose the best model

        Args:
            audio_path: Path to audio file
            language: Target language (if known)
            use_indonesian_model: Whether to use Indonesian model for ID language

        Returns:
            Dict with transcription, segments, language, and model_used
        """
        try:
            # If language not specified, detect it
            if language is None:
                language = self.detect_language(audio_path)

            # Use Indonesian model if it's Indonesian language and enabled
            if language == "id" and use_indonesian_model and settings.USE_INDONESIAN_MODEL:
                try:
                    logger.info("Using Indonesian Wav2vec model for transcription")
                    return self.transcribe_with_indonesian_model(audio_path)
                except Exception as e:
                    logger.warning(f"Indonesian model failed, falling back to Whisper: {e}")
                    return self.transcribe_with_whisper(audio_path, language="id")
            else:
                # Use Whisper for other languages or as fallback
                return self.transcribe_with_whisper(audio_path, language=language)

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def get_models_status(self) -> Dict[str, bool]:
        """Get status of loaded models"""
        return {
            "whisper": self.whisper_model is not None,
            "indonesian_wav2vec": self.indonesian_model is not None
        }


# Global instance
stt_service = STTService()
