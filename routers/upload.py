from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from typing import Optional
import logging

from ..database import get_db
from ..models import Call
from ..schemas import CallCreate, CallResponse, ErrorResponse
from ..services.storage import save_audio_file
from ..tasks import process_call

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=CallResponse, responses={400: {"model": ErrorResponse}})
async def upload_file(
    file: UploadFile,
    agent_id: str = Form(...),
    customer_id: Optional[str] = Form(None),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.wav', '.mp3', '.ogg')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only WAV, MP3, and OGG files are supported."
            )

        # Generate unique ID for the call
        call_id = uuid.uuid4()
        
        # Create call record in database
        call = Call(
            id=call_id,
            agent_id=agent_id,
            customer_id=customer_id,
            language=language,
            audio_path=f"audio/{call_id}.{file.filename.split('.')[-1]}"
        )
        db.add(call)
        db.commit()

        try:
            # Save the uploaded file
            file_path = await save_audio_file(file, call_id)
            
            # Update call record with file path
            call.audio_path = file_path
            call.processing_status = "pending"
            db.commit()

            # Trigger background processing
            process_call.delay(str(call_id))

            return CallResponse(
                message="File uploaded successfully",
                call_id=call_id,
                status="pending"
            )

        except Exception as e:
            # If file saving fails, update call status
            call.processing_status = "failed"
            call.error_message = str(e)
            db.commit()
            logger.error(f"Error processing file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during file upload"
        ) 