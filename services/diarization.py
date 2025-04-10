import os
import logging
from typing import List, Dict, Any
import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.speaker_diarization import SpeakerDiarization
import numpy as np

logger = logging.getLogger(__name__)

class DiarizationService:
    def __init__(self):
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")

    def load_pipeline(self):
        """
        Load the speaker diarization pipeline
        """
        try:
            if not self.pipeline:
                logger.info("Loading speaker diarization pipeline")
                self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization",
                    use_auth_token=os.getenv("HUGGINGFACE_TOKEN"),
                    device=self.device
                )
                logger.info("Pipeline loaded successfully")
        except Exception as e:
            logger.error(f"Error loading pipeline: {str(e)}")
            raise

    def diarize_audio(
        self,
        file_path: str,
        num_speakers: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Perform speaker diarization on an audio file
        Returns a list of segments with speaker information
        """
        try:
            if not self.pipeline:
                self.load_pipeline()

            # Apply the pipeline to the audio file
            diarization = self.pipeline(
                file_path,
                num_speakers=num_speakers
            )

            # Convert diarization output to segments
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                segment = {
                    "speaker": speaker,
                    "start_time": turn.start,
                    "end_time": turn.end,
                    "text": "",  # Will be filled by transcription
                    "confidence": 1.0  # Default confidence
                }
                segments.append(segment)

            # Sort segments by start time
            segments.sort(key=lambda x: x["start_time"])

            return segments

        except Exception as e:
            logger.error(f"Error performing diarization: {str(e)}")
            raise

    def assign_speaker_types(
        self,
        segments: List[Dict[str, Any]],
        agent_id: str
    ) -> List[Dict[str, Any]]:
        """
        Assign speaker types (agent/customer) based on the agent_id
        """
        try:
            # Get unique speakers
            speakers = list(set(seg["speaker"] for seg in segments))
            
            # If we have exactly 2 speakers, assign types
            if len(speakers) == 2:
                # Assume the first speaker is the agent
                speaker_types = {
                    speakers[0]: "agent",
                    speakers[1]: "customer"
                }
            else:
                # If we have more or fewer speakers, mark all as unknown
                speaker_types = {speaker: "unknown" for speaker in speakers}

            # Update segments with speaker types
            for segment in segments:
                segment["speaker_type"] = speaker_types[segment["speaker"]]

            return segments

        except Exception as e:
            logger.error(f"Error assigning speaker types: {str(e)}")
            raise

# Create a singleton instance
diarization_service = DiarizationService()

# Export the diarize_audio function for use in tasks
def diarize_audio(file_path: str, num_speakers: int = 2) -> List[Dict[str, Any]]:
    return diarization_service.diarize_audio(file_path, num_speakers)

def assign_speaker_types(segments: List[Dict[str, Any]], agent_id: str) -> List[Dict[str, Any]]:
    return diarization_service.assign_speaker_types(segments, agent_id) 