# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    entries: List["JournalEntry"] = []

    class Config:
        orm_mode = True

class JournalEntryBase(BaseModel):
    title: str
    content: str

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntry(JournalEntryBase):
    id: int
    timestamp: datetime
    owner_id: int

    class Config:
        orm_mode = True
