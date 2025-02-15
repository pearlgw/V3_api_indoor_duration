from datetime import datetime
from fastapi import status
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

def fetch_all_service(db: Session):
    query = select(User).where(User.roles == 'user')
    result = db.execute(query)
    user_assistans = result.scalars().all()
    return user_assistans

def update_status_embed_service(uid_assistant, db:Session, current_user):
    data_assistant = db.query(User).filter(User.uid == uid_assistant).first()
    
    if not data_assistant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data tidak ditemukan")
    
    data_assistant.status_embed = True
    
    log_fullname = current_user.get("fullname")
    action_data = f"{log_fullname} updated status_embed user assistant: {data_assistant.dict()}"
    format_all_logs(db, log_fullname, action_data)
    
    db.commit()
    return {
        "uid": data_assistant.uid,
        "fullname": data_assistant.fullname,
        "status_embed": data_assistant.status_embed
    }