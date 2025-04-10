import os
import logging
from typing import Tuple
import librosa
import numpy as np
from pydub import AudioSegment
import tempfile

logger = logging.getLogger(__name__)

class SilenceAnalysisService:
    def __init__(self):
        self.silence_threshold = -40  # dB
        self.min_silence_len = 1000  # ms
        self.hold_time_threshold = 2000  # ms

    def detect_silence(
        self,
        file_path: str,
        segments: list
    ) -> Tuple[float, float]:
        """
        Detect silence periods in the audio file
        Returns total hold time and dead air time in seconds
        """
        try:
            # Load audio file
            audio = AudioSegment.from_file(file_path)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Detect silent chunks
            silent_chunks = self._detect_silent_chunks(audio)
            
            # Calculate hold time and dead air time
            hold_time, dead_air_time = self._analyze_silence(
                silent_chunks,
                segments,
                audio.duration_seconds
            )
            
            return hold_time, dead_air_time

        except Exception as e:
            logger.error(f"Error detecting silence: {str(e)}")
            raise

    def _detect_silent_chunks(self, audio: AudioSegment) -> list:
        """
        Detect silent chunks in the audio
        """
        try:
            # Split audio into chunks
            chunks = librosa.effects.split(
                np.array(audio.get_array_of_samples()),
                top_db=-self.silence_threshold,
                frame_length=1024,
                hop_length=512
            )
            
            # Convert chunks to milliseconds
            silent_chunks = []
            for start, end in chunks:
                start_ms = start * 1000 / audio.frame_rate
                end_ms = end * 1000 / audio.frame_rate
                if end_ms - start_ms >= self.min_silence_len:
                    silent_chunks.append((start_ms, end_ms))
            
            return silent_chunks

        except Exception as e:
            logger.error(f"Error detecting silent chunks: {str(e)}")
            raise

    def _analyze_silence(
        self,
        silent_chunks: list,
        segments: list,
        total_duration: float
    ) -> Tuple[float, float]:
        """
        Analyze silence periods to determine hold time and dead air time
        """
        try:
            hold_time = 0.0
            dead_air_time = 0.0
            
            # Convert segments to time ranges
            segment_ranges = [
                (seg["start_time"] * 1000, seg["end_time"] * 1000)
                for seg in segments
            ]
            
            for start_ms, end_ms in silent_chunks:
                duration_ms = end_ms - start_ms
                
                # Check if silence is during a segment
                is_during_segment = False
                for seg_start, seg_end in segment_ranges:
                    if start_ms >= seg_start and end_ms <= seg_end:
                        is_during_segment = True
                        break
                
                if is_during_segment:
                    # If silence is during a segment, it's dead air
                    dead_air_time += duration_ms / 1000
                else:
                    # If silence is between segments, it's hold time
                    hold_time += duration_ms / 1000
            
            return hold_time, dead_air_time

        except Exception as e:
            logger.error(f"Error analyzing silence: {str(e)}")
            raise

# Create a singleton instance
silence_analysis_service = SilenceAnalysisService()

# Export the detect_silence function for use in tasks
def detect_silence(file_path: str, segments: list) -> Tuple[float, float]:
    return silence_analysis_service.detect_silence(file_path, segments) 