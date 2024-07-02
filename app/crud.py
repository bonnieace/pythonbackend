# app/crud.py
from sqlalchemy.orm import Session
from app.models import User, JournalEntry
from app.schemas import UserCreate, JournalEntryCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_entry(db: Session, entry: JournalEntryCreate, user_id: int):
    db_entry = JournalEntry(**entry.dict(), owner_id=user_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_entries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(JournalEntry).offset(skip).limit(limit).all()
