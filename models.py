from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class CallRecording(Base):
    __tablename__ = "call_recordings"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)
    file_path = Column(String(512))
    duration = Column(Float)
    status = Column(String(50))  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transcriptions = relationship("Transcription", back_populates="recording")
    silence_analysis = relationship("SilenceAnalysis", back_populates="recording")
    overtalk_analysis = relationship("OvertalkAnalysis", back_populates="recording")

class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("call_recordings.id"))
    text = Column(Text)
    confidence = Column(Float)
    language = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    recording = relationship("CallRecording", back_populates="transcriptions")

class SilenceAnalysis(Base):
    __tablename__ = "silence_analysis"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("call_recordings.id"))
    total_silence_duration = Column(Float)
    silence_percentage = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    recording = relationship("CallRecording", back_populates="silence_analysis")

class OvertalkAnalysis(Base):
    __tablename__ = "overtalk_analysis"

    id = Column(Integer, primary_key=True, index=True)
    recording_id = Column(Integer, ForeignKey("call_recordings.id"))
    total_overtalk_duration = Column(Float)
    overtalk_percentage = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    recording = relationship("CallRecording", back_populates="overtalk_analysis") 