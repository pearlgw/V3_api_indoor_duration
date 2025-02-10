from datetime import datetime
import json
from uuid import UUID
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from utils.utils import hash_password
from sqlmodel import Session, select
from model.user import User
from utils.utils import get_current_user
from utils.enkripsi_gambar import save_encrypted_image
from .log import format_all_logs

load_dotenv()

def create_user_service(nim, fullname, address, email, password, image, db: Session, current_user):
    existing_user = db.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah digunakan")
    
    hashed_password = hash_password(password)
    
    try:
        image_path = save_encrypted_image(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan gambar: {str(e)}")
        
    new_user = User(
        nim= nim,
        fullname= fullname,
        address= address,
        email= email,
        hashed_password= hashed_password,
        image= image_path
    )
    
    log_fullname = current_user.get("fullname")
    action_data = f"{log_fullname} created data assistant: {new_user.dict()}"
    format_all_logs(db, log_fullname, action_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user