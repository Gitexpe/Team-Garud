import os
import logging
from celery import Celery
from sqlalchemy.orm import Session
import uuid
import time

from database import SessionLocal
from models import Call, Segment
from services.transcription import transcribe_audio
from services.diarization import diarize_audio, assign_speaker_types
from services.sentiment import analyze_segments, get_sentiment_summary
from services.silence_analysis import detect_silence
from services.overtalk import detect_overtalk, get_overtalk_summary

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Celery
celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

@celery.task
def test_task(message: str):
    """Test task to verify Celery is working"""
    logger.info(f"Received test message: {message}")
    time.sleep(2)  # Simulate some work
    return f"Processed message: {message}"

@celery.task(bind=True, max_retries=3)
def process_call(self, call_id: str):
    """
    Process a call recording in the background
    """
    db = SessionLocal()
    try:
        # Get call record
        call = db.query(Call).filter(Call.id == uuid.UUID(call_id)).first()
        if not call:
            raise ValueError(f"Call with ID {call_id} not found")

        # Update status to processing
        call.processing_status = "processing"
        db.commit()

        try:
            # 1. Transcribe audio
            transcription, duration = transcribe_audio(
                call.audio_path,
                call.language
            )
            call.transcription = transcription
            call.duration = duration
            db.commit()

            # 2. Perform speaker diarization
            segments = diarize_audio(call.audio_path)
            segments = assign_speaker_types(segments, call.agent_id)

            # 3. Analyze sentiment
            segments = analyze_segments(segments, call.language)
            sentiment_summary = get_sentiment_summary(segments)

            # 4. Detect silence
            hold_time, dead_air_time = detect_silence(call.audio_path, segments)
            call.hold_time = hold_time
            call.dead_air_time = dead_air_time

            # 5. Detect overtalk
            overtalk_count = detect_overtalk(segments)
            call.overtalk_count = overtalk_count

            # Save segments to database
            for segment in segments:
                db_segment = Segment(
                    id=uuid.uuid4(),
                    call_id=call.id,
                    speaker=segment["speaker"],
                    start_time=segment["start_time"],
                    end_time=segment["end_time"],
                    text=segment["text"],
                    sentiment=segment.get("sentiment"),
                    confidence=segment.get("confidence"),
                    speaker_type=segment.get("speaker_type")
                )
                db.add(db_segment)

            # Update call status to completed
            call.processing_status = "completed"
            db.commit()

            logger.info(f"Successfully processed call {call_id}")

        except Exception as e:
            # Update call status to failed
            call.processing_status = "failed"
            call.error_message = str(e)
            db.commit()
            logger.error(f"Error processing call {call_id}: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Unexpected error processing call {call_id}: {str(e)}")
        raise

    finally:
        db.close()

@celery.task
def cleanup_old_calls(days: int = 30):
    """
    Clean up old call records and their associated files
    """
    db = SessionLocal()
    try:
        # Get calls older than specified days
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_calls = db.query(Call).filter(
            Call.created_at < cutoff_date,
            Call.is_deleted == False
        ).all()

        for call in old_calls:
            try:
                # Mark call as deleted
                call.is_deleted = True
                db.commit()
                
                # Delete associated files
                if os.path.exists(call.audio_path):
                    os.remove(call.audio_path)
                
                logger.info(f"Cleaned up call {call.id}")
                
            except Exception as e:
                logger.error(f"Error cleaning up call {call.id}: {str(e)}")
                db.rollback()

    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")
        raise

    finally:
        db.close() 