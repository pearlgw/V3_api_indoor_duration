from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select
from db.database import get_db
from service.log import get_all_logs
from utils.utils import get_current_user, format_response

log_router = APIRouter()

@log_router.get("/")
def get_all_person_duration(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
    try:
        get_logs = get_all_logs(db)
        return format_response(status.HTTP_200_OK, "Berhasil", get_logs)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))