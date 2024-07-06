# app/routers/auth.py
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.core.security import verify_password, oauth2_scheme, authenticate_user, create_access_token
from app.models import User  # Assuming you have a User model defined
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password


router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
 

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup(username: str, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    # Create the user in the database
    new_user = User(username=username, hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Optionally, generate and return an access token for the newly registered user
    access_token = create_access_token(data={"sub": new_user['username']})
    return {"access_token": access_token, "token_type": "bearer"}
