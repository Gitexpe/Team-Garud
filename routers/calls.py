from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from ..database import get_db
from ..models import Call
from ..schemas import CallBase, ErrorResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/calls/{call_id}", response_model=CallBase, responses={404: {"model": ErrorResponse}})
async def get_call(
    call_id: str,
    db: Session = Depends(get_db)
):
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if not call:
            raise HTTPException(
                status_code=404,
                detail=f"Call with ID {call_id} not found"
            )
        return call
    except Exception as e:
        logger.error(f"Error retrieving call {call_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the call"
        )

@router.get("/calls", response_model=List[CallBase])
async def get_calls(
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering"),
    status: Optional[str] = Query(None, description="Filter by processing status"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Call)
        
        if agent_id:
            query = query.filter(Call.agent_id == agent_id)
        
        if start_date:
            query = query.filter(Call.created_at >= start_date)
        
        if end_date:
            query = query.filter(Call.created_at <= end_date)
        
        if status:
            query = query.filter(Call.processing_status == status)
        
        return query.order_by(Call.created_at.desc()).all()
    
    except Exception as e:
        logger.error(f"Error retrieving calls: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving calls"
        )

@router.delete("/calls/{call_id}", responses={404: {"model": ErrorResponse}})
async def delete_call(
    call_id: str,
    db: Session = Depends(get_db)
):
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if not call:
            raise HTTPException(
                status_code=404,
                detail=f"Call with ID {call_id} not found"
            )
        
        # Soft delete
        call.is_deleted = True
        db.commit()
        
        return {"message": f"Call {call_id} marked as deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting call {call_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the call"
        ) 