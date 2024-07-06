from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import bcrypt

# Define the FastAPI app
app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class JournalEntry(BaseModel):
    id: int
    title: str
    content: str
    category: str
    date: datetime

class JournalEntryCreate(BaseModel):
    title: str
    content: str
    category: str

class Signup(BaseModel):
    username: str
    password: str

# Example database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": None,
        "disabled": False,
    }
}

# Example password
password = "password"

# Hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

# Update the fake_users_db with hashed password
fake_users_db["johndoe"]["hashed_password"] = hashed_password

fake_entries_db = [
    {
        "id": 1, "title": "Day at the Beach", "content": "Today was a great day...",
        "category": "leisure", "date": datetime(2023, 7, 1, 10, 0)
    },
    {
        "id": 2, "title": "Grocery Shopping", "content": "Bought some fresh fruits...",
        "category": "daily", "date": datetime(2023, 7, 2, 14, 30)
    },
]

# Security setup
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to handle user signup
def create_user(signup_data: Signup):
    hashed_password = get_password_hash(signup_data.password)
    if signup_data.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    fake_users_db[signup_data.username] = {
        "username": signup_data.username,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    return {"message": "User created successfully"}

# Signup route
@app.post("/signup", response_model=dict)
async def signup(signup_data: Signup):
    return create_user(signup_data)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return UserInDB(**user)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return UserInDB(**user)

# Routes
@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/entries/", response_model=List[JournalEntry])
async def read_entries(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)):
    user_entries = [
        JournalEntry(id=entry["id"], title=entry["title"], content=entry["content"],
                     category=entry["category"], date=entry["date"])
        for entry in fake_entries_db
        if entry.get("username") == current_user.username
    ]
    return user_entries[skip : skip + limit]
@app.get("/entries/{entry_id}", response_model=JournalEntry)
async def read_entry(entry_id: int, current_user: User = Depends(get_current_user)):
    entry = next((JournalEntry(id=entry["id"], title=entry["title"], content=entry["content"],
                     category=entry["category"], date=entry["date"]) for entry in fake_entries_db
                     if entry["id"] == entry_id and entry.get("username") == current_user.username), None)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found or unauthorized to access"
        )
    return entry
@app.post("/entries/", response_model=JournalEntry)
async def create_entry(entry: JournalEntryCreate, current_user: User = Depends(get_current_user)):
    new_entry = {
        "id": len(fake_entries_db) + 1,
        "title": entry.title,
        "content": entry.content,
        "category": entry.category,
        "date": datetime.utcnow(),  # Set the date to the current time
        "username": current_user.username  # Associate the entry with the current user
    }
    fake_entries_db.append(new_entry)
    return new_entry

@app.put("/entries/{entry_id}", response_model=JournalEntry)
async def update_entry(entry_id: int, entry_update: JournalEntryCreate, current_user: User = Depends(get_current_user)):
    # Find the entry in fake_entries_db by entry_id and check ownership
    for entry in fake_entries_db:
        if entry["id"] == entry_id and entry.get("username") == current_user.username:
            entry.update({
                "title": entry_update.title,
                "content": entry_update.content,
                "category": entry_update.category,
                "date": datetime.utcnow(),  # Update the date to the current time
            })
            return entry
    # If entry_id not found or unauthorized, raise HTTPException
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Journal entry not found or unauthorized to update"
    )

@app.delete("/entries/{entry_id}", response_model=dict)
async def delete_entry(entry_id: int, current_user: User = Depends(get_current_user)):
    # Find and delete the entry from fake_entries_db if owned by current_user
    for idx, entry in enumerate(fake_entries_db):
        if entry["id"] == entry_id and entry.get("username") == current_user.username:
            del fake_entries_db[idx]
            return {"message": "Journal entry deleted successfully"}
    # If entry_id not found or unauthorized, raise HTTPException
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Journal entry not found or unauthorized to delete"
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.100.2", port=8000)
