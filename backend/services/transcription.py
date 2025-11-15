"""
Transcription Service - Hybrid STT using Whisper + Indonesian Wav2vec
"""

import os
import logging
from typing import Optional, Dict, Any
import torch
import numpy as np

logger = logging.getLogger(__name__)


class TranscriptionService:
    """
    Hybrid transcription service that intelligently routes between:
    - Indonesian Wav2vec 2.0 (for pure Indonesian - 4.27% WER)
    - Whisper Turbo (for multilingual/mixed languages)
    """

    def __init__(self):
        self.whisper_model = None
        self.wav2vec_processor = None
        self.wav2vec_model = None
        self.whisper_available = False
        self.wav2vec_available = False

        # Initialize models
        self._init_whisper()
        self._init_wav2vec()

    def _init_whisper(self):
        """Initialize Whisper model"""
        try:
            import whisper

            # Use turbo model (recommended in research: 8x speed, good accuracy)
            model_size = os.getenv("WHISPER_MODEL", "turbo")
            logger.info(f"Loading Whisper model: {model_size}")

            self.whisper_model = whisper.load_model(model_size)
            self.whisper_available = True

            logger.info(f"Whisper model '{model_size}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper: {e}")
            self.whisper_available = False

    def _init_wav2vec(self):
        """Initialize Indonesian Wav2vec 2.0 model"""
        try:
            from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

            model_name = "indonesian-nlp/wav2vec2-large-xlsr-indonesian"
            logger.info(f"Loading Indonesian Wav2vec model: {model_name}")

            self.wav2vec_processor = Wav2Vec2Processor.from_pretrained(model_name)
            self.wav2vec_model = Wav2Vec2ForCTC.from_pretrained(model_name)

            # Move to GPU if available
            if torch.cuda.is_available():
                self.wav2vec_model = self.wav2vec_model.to("cuda")
                logger.info("Wav2vec model moved to GPU")

            self.wav2vec_available = True
            logger.info("Indonesian Wav2vec model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Wav2vec: {e}")
            self.wav2vec_available = False

    async def transcribe(
        self,
        audio_path: str,
        language: str = "auto",
        model_preference: str = "auto"
    ) -> Dict[str, Any]:
        """
        Transcribe audio file using intelligent model selection

        Args:
            audio_path: Path to audio file
            language: Language code (auto, id, en) or "auto" for detection
            model_preference: Which model to prefer (auto, whisper, wav2vec)

        Returns:
            Dictionary with transcription results
        """
        # Detect language if not specified
        if language == "auto":
            language = await self._detect_language(audio_path)
            logger.info(f"Detected language: {language}")

        # Choose appropriate model
        model_to_use = self._select_model(language, model_preference)
        logger.info(f"Using model: {model_to_use} for language: {language}")

        # Perform transcription
        if model_to_use == "wav2vec" and self.wav2vec_available:
            result = await self._transcribe_wav2vec(audio_path)
        elif self.whisper_available:
            result = await self._transcribe_whisper(audio_path, language)
        else:
            raise RuntimeError("No transcription models available")

        result["language"] = language
        result["model_used"] = model_to_use

        return result

    def _select_model(self, language: str, preference: str) -> str:
        """
        Select the best model based on language and preference

        Strategy from research:
        - Pure Indonesian -> Wav2vec (4.27% WER)
        - Mixed/Other languages -> Whisper (multilingual support)
        """
        if preference == "whisper":
            return "whisper"
        elif preference == "wav2vec":
            return "wav2vec"

        # Auto selection
        if language == "id" and self.wav2vec_available:
            # Use Wav2vec for Indonesian (superior accuracy)
            return "wav2vec"
        elif self.whisper_available:
            # Use Whisper for everything else
            return "whisper"
        elif self.wav2vec_available:
            # Fallback to Wav2vec if Whisper not available
            return "wav2vec"
        else:
            raise RuntimeError("No models available")

    async def _detect_language(self, audio_path: str) -> str:
        """
        Detect language using Whisper's built-in detection
        (Uses tiny model for fast detection)
        """
        if not self.whisper_available:
            return "id"  # Default to Indonesian

        try:
            import whisper

            # Use tiny model for fast language detection
            tiny_model = whisper.load_model("tiny")

            # Load audio and detect language
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)

            # Make log-Mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(tiny_model.device)

            # Detect language
            _, probs = tiny_model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)

            logger.info(f"Language detection: {detected_lang} (confidence: {probs[detected_lang]:.2f})")

            return detected_lang
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return "id"  # Default to Indonesian

    async def _transcribe_whisper(self, audio_path: str, language: str) -> Dict[str, Any]:
        """Transcribe using Whisper"""
        try:
            logger.info(f"Transcribing with Whisper (language: {language})")

            # Transcribe
            result = self.whisper_model.transcribe(
                audio_path,
                language=language if language != "auto" else None,
                task="transcribe",
                verbose=False
            )

            return {
                "text": result["text"].strip(),
                "segments": [
                    {
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": seg["text"].strip()
                    }
                    for seg in result.get("segments", [])
                ],
                "duration": result.get("segments", [])[-1]["end"] if result.get("segments") else 0
            }
        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            raise

    async def _transcribe_wav2vec(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe using Indonesian Wav2vec 2.0"""
        try:
            import librosa

            logger.info("Transcribing with Indonesian Wav2vec")

            # Load audio
            audio_array, sampling_rate = librosa.load(audio_path, sr=16000)

            # Process audio
            inputs = self.wav2vec_processor(
                audio_array,
                sampling_rate=16000,
                return_tensors="pt",
                padding=True
            )

            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}

            # Generate transcription
            with torch.no_grad():
                logits = self.wav2vec_model(inputs.input_values).logits

            # Decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.wav2vec_processor.batch_decode(predicted_ids)[0]

            # Calculate duration
            duration = len(audio_array) / sampling_rate

            return {
                "text": transcription.strip(),
                "segments": None,  # Wav2vec doesn't provide timestamps
                "duration": duration
            }
        except Exception as e:
            logger.error(f"Wav2vec transcription failed: {e}")
            raise
