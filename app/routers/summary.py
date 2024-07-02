# app/routers/summary.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.core.database import get_db
from app.schemas import JournalEntry
from typing import List
from app.models import User


router = APIRouter()

@router.get("/summary", response_model=List[JournalEntry])
def get_summary(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = db.query(JournalEntry).filter(JournalEntry.owner_id == current_user.id).offset(skip).limit(limit).all()
    return entries
