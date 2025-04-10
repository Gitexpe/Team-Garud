import os
import logging
import whisper
from typing import Tuple, Optional
import torch

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

    def load_model(self, model_name: str = "medium"):
        """
        Load the Whisper model
        """
        try:
            if not self.model:
                logger.info(f"Loading Whisper model: {model_name}")
                self.model = whisper.load_model(
                    model_name,
                    device=self.device,
                    download_root="models/whisper"
                )
                logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def transcribe_audio(
        self,
        file_path: str,
        language: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Transcribe an audio file using Whisper
        Returns the transcription text and duration
        """
        try:
            if not self.model:
                self.load_model()

            # Load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(file_path)
            audio = whisper.pad_or_trim(audio)

            # Make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            # Detect the spoken language
            if not language:
                _, probs = self.model.detect_language(mel)
                language = max(probs, key=probs.get)
                logger.info(f"Detected language: {language}")

            # Decode the audio
            options = whisper.DecodingOptions(
                language=language,
                fp16=False if self.device == "cpu" else True
            )
            result = whisper.decode(self.model, mel, options)

            return result.text, len(audio) / 16000  # Duration in seconds

        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise

# Create a singleton instance
transcription_service = TranscriptionService()

# Export the transcribe_audio function for use in tasks
def transcribe_audio(file_path: str, language: Optional[str] = None) -> Tuple[str, float]:
    return transcription_service.transcribe_audio(file_path, language) 