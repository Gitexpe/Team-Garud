from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import uuid

class SegmentBase(BaseModel):
    speaker: str
    start_time: float
    end_time: float
    text: str
    sentiment: Optional[str] = None
    confidence: Optional[float] = None
    speaker_type: Optional[str] = None

    @validator('start_time', 'end_time')
    def validate_times(cls, v):
        if v < 0:
            raise ValueError('Time values cannot be negative')
        return v

class CallBase(BaseModel):
    id: uuid.UUID
    agent_id: str
    customer_id: Optional[str] = None
    created_at: datetime
    duration: Optional[float] = None
    hold_time: float = 0.0
    dead_air_time: float = 0.0
    overtalk_count: int = 0
    transcription: Optional[str] = None
    audio_path: str
    processing_status: str
    error_message: Optional[str] = None
    language: str = "en"
    segments: List[SegmentBase] = []

    class Config:
        orm_mode = True

class CallCreate(BaseModel):
    agent_id: str
    customer_id: Optional[str] = None
    language: str = "en"

class CallUpdate(BaseModel):
    processing_status: Optional[str] = None
    error_message: Optional[str] = None
    transcription: Optional[str] = None
    duration: Optional[float] = None
    hold_time: Optional[float] = None
    dead_air_time: Optional[float] = None
    overtalk_count: Optional[int] = None

class CallResponse(BaseModel):
    message: str
    call_id: uuid.UUID
    status: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None 