import logging
from typing import List, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

class OvertalkService:
    def __init__(self):
        self.min_overlap_duration = 0.5  # seconds
        self.confidence_threshold = 0.7

    def detect_overtalk(
        self,
        segments: List[Dict[str, Any]]
    ) -> int:
        """
        Detect overlapping speech segments
        Returns the count of overtalk instances
        """
        try:
            # Sort segments by start time
            sorted_segments = sorted(segments, key=lambda x: x["start_time"])
            
            # Initialize overtalk count
            overtalk_count = 0
            
            # Compare each segment with the next one
            for i in range(len(sorted_segments) - 1):
                current_seg = sorted_segments[i]
                next_seg = sorted_segments[i + 1]
                
                # Check if segments overlap
                if self._is_overlapping(current_seg, next_seg):
                    # Check if speakers are different
                    if current_seg["speaker"] != next_seg["speaker"]:
                        # Check if overlap duration is significant
                        overlap_duration = self._get_overlap_duration(
                            current_seg,
                            next_seg
                        )
                        if overlap_duration >= self.min_overlap_duration:
                            overtalk_count += 1
            
            return overtalk_count

        except Exception as e:
            logger.error(f"Error detecting overtalk: {str(e)}")
            raise

    def _is_overlapping(
        self,
        seg1: Dict[str, Any],
        seg2: Dict[str, Any]
    ) -> bool:
        """
        Check if two segments overlap in time
        """
        try:
            return seg1["end_time"] > seg2["start_time"]
        except Exception as e:
            logger.error(f"Error checking segment overlap: {str(e)}")
            raise

    def _get_overlap_duration(
        self,
        seg1: Dict[str, Any],
        seg2: Dict[str, Any]
    ) -> float:
        """
        Calculate the duration of overlap between two segments
        """
        try:
            overlap_start = max(seg1["start_time"], seg2["start_time"])
            overlap_end = min(seg1["end_time"], seg2["end_time"])
            return max(0, overlap_end - overlap_start)
        except Exception as e:
            logger.error(f"Error calculating overlap duration: {str(e)}")
            raise

    def get_overtalk_summary(
        self,
        segments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a summary of overtalk analysis
        """
        try:
            overtalk_count = self.detect_overtalk(segments)
            
            # Calculate total call duration
            if segments:
                total_duration = max(seg["end_time"] for seg in segments)
            else:
                total_duration = 0.0
            
            # Calculate overtalk percentage
            overtalk_percentage = (
                (overtalk_count * self.min_overlap_duration / total_duration * 100)
                if total_duration > 0 else 0.0
            )
            
            return {
                "overtalk_count": overtalk_count,
                "total_duration": total_duration,
                "overtalk_percentage": overtalk_percentage,
                "min_overlap_duration": self.min_overlap_duration
            }

        except Exception as e:
            logger.error(f"Error generating overtalk summary: {str(e)}")
            raise

# Create a singleton instance
overtalk_service = OvertalkService()

# Export functions for use in tasks
def detect_overtalk(segments: List[Dict[str, Any]]) -> int:
    return overtalk_service.detect_overtalk(segments)

def get_overtalk_summary(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    return overtalk_service.get_overtalk_summary(segments) 