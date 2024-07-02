# app/routers/entries.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import JournalEntry, JournalEntryCreate
from app.crud import create_user_entry, get_entries
from app.dependencies import get_current_user
from app.core.database import get_db
from app.models import User

router = APIRouter()

@router.post("/", response_model=JournalEntry)
def create_entry(entry: JournalEntryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_user_entry(db=db, entry=entry, user_id=current_user.id)

@router.get("/", response_model=List[JournalEntry])
def read_entries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = get_entries(db, skip=skip, limit=limit)
    return entries
