from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session
from model.user_token import UserToken
from utils.utils import get_current_user  # Misalnya untuk verifikasi token
from db.database import get_db
from sqlmodel import select
from datetime import datetime

def verify_token_validity(
    current_user: dict = Depends(get_current_user), 
    authorization: str = Header(None, include_in_schema=False),  # Mengambil header authorization
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=400, detail="Token tidak ditemukan")
    
    # Cek apakah token memiliki format yang benar 'Bearer <token>'
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Format token tidak valid")
    
    # Ambil token setelah 'Bearer'
    token = authorization[7:]  # Memotong 'Bearer ' untuk mendapatkan tokennya

    # Cek apakah token ada di database dan valid
    user_token = db.exec(select(UserToken).where(UserToken.token == token)).first()
    
    if not user_token:
        raise HTTPException(status_code=401, detail="Token sudah tidak valid atau sudah dihapus")
    
    
    return user_token