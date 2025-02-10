from passlib.context import CryptContext
from fastapi import HTTPException, status, Security, Depends
from sqlmodel import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from sqlalchemy.orm import Session
from db.database import get_db
from model.user import User
from model.user_token import UserToken
from typing import Optional, List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# hash and password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# buat jwt token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        # Verifikasi token dan ambil data payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        role = payload.get("role")
        fullname = payload.get("fullname")
        if email is None:
            raise HTTPException(status_code=401, detail="Token tidak valid")
        
        # Cek apakah token ada di database
        user_token = db.exec(select(UserToken).where(UserToken.token == token)).first()
        if not user_token:
            raise HTTPException(status_code=401, detail="Token sudah tidak valid")
        
        # Ambil data user dari database
        user = db.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Pengguna tidak ditemukan")
        
        if user_token.expires_at < datetime.now():
            raise HTTPException(status_code=401, detail="Token kadaluwarsa")
        
        return {"email": email, "role": role, "fullname": fullname}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token tidak valid")

def format_response(status_code: str, message: str, data= None, error=None):
    return {
        "meta": {
            "message": message,
            "status_code": status_code,
            "message_error": error
        },
        "data": data
    }
    
def convert_seconds_to_time(seconds: float) -> str:
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return str(timedelta(hours=hours, minutes=minutes, seconds=seconds))