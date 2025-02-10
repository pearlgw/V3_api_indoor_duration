from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException, Response
from sqlalchemy.orm import Session
from db.database import get_db
from service.admin import create_user_service
from utils.utils import get_current_user, format_response
from utils.enkripsi_gambar import decrypt_image
from service.log import format_all_logs
from cryptography.fernet import Fernet
import os
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(ENCRYPTION_KEY)

admin_router = APIRouter()

@admin_router.post("/create")
def create_user_enkrip_image(
    nim: str = Form(...),
    fullname: str = Form(...),
    address: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Cek apakah user yang mengakses adalah admin
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
    try:
        new_user = create_user_service(
            nim=nim,
            fullname=fullname,
            address=address,
            email=email,
            password=password,
            image=image,
            db=db,
            current_user=current_user
        )
        return format_response(status.HTTP_201_CREATED, "Data berhasil dibuat", new_user)
    
    except HTTPException as e:
        return format_response(e.status_code, "Data gagal dibuat", error=e.detail)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))