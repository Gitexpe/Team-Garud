from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime
from database import Base

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    duration = Column(Float, nullable=True)
    hold_time = Column(Float, default=0.0)
    dead_air_time = Column(Float, default=0.0)
    overtalk_count = Column(Integer, default=0)
    transcription = Column(Text, nullable=True)
    audio_path = Column(String, nullable=False)
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    language = Column(String, default="en")
    is_deleted = Column(Boolean, default=False)
    
    segments = relationship("Segment", back_populates="call", cascade="all, delete-orphan")

class Segment(Base):
    __tablename__ = "segments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id", ondelete="CASCADE"))
    speaker = Column(String, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    sentiment = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    speaker_type = Column(String, nullable=True)  # agent, customer, system
    
    call = relationship("Call", back_populates="segments") 