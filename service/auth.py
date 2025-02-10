from fastapi import HTTPException
from utils.utils import verify_password, create_access_token
from sqlmodel import Session, select
from model.user import User
from model.user_token import UserToken
from datetime import timedelta, datetime
from config.config import ACCESS_TOKEN_EXPIRE_DAYS
from .log import format_all_logs

def login_service(form_data, db: Session):
    user = db.exec(select(User).where(User.email == form_data.email)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Username atau password salah")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Password salah")
    
    if user.token != form_data.verification_token:
        raise HTTPException(status_code=400, detail="Token verifikasi salah")
    
    expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={
            "email": user.email, 
            "role": user.roles,
            "fullname": user.fullname
        }, 
        expires_delta=expires
    )
    
    created_at = datetime.now()
    expires_at = created_at + expires
    
    user_token = UserToken(user_uid=user.uid, token=access_token, expires_at=expires_at)
    
    action_data = f"role {user.roles} login: {user.dict()}"
    format_all_logs(db, user.fullname, action_data)
    
    db.add(user_token)
    db.commit()
    
    return {
        "fullname": user.fullname, 
        "email": user.email, 
        "access_token": access_token, 
        "token_type": "bearer"
    }

def logout_service(token: str, db: Session):
    # Cek apakah token ada di database
    user_token = db.exec(select(UserToken).where(UserToken.token == token)).first()
    
    if not user_token:
        raise HTTPException(status_code=400, detail="Token tidak valid atau sudah logout")
    
    user = db.exec(select(User).where(User.uid == user_token.user_uid)).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Pengguna tidak ditemukan")

    # Catat log logout
    action_data = f"User {user.email} logout pada {datetime.now()}"
    format_all_logs(db, user.fullname, action_data)
    
    # Hapus token dari database
    db.delete(user_token)
    db.commit()
    return "Logout berhasil"