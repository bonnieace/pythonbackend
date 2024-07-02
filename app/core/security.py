from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
import bcrypt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

print("Updated fake_users_db:")
print(fake_users_db)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
# Password handling
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Token handling
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    print(f"--------------------------------Using SECRET_KEY: {settings.SECRET_KEY}")

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Authentication logic
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None
