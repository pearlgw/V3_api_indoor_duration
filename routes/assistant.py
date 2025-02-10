from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from service.assistant import fetch_all_person_duration
from utils.utils import get_current_user, format_response

assistant_router = APIRouter()

@assistant_router.get("/detail")
def get_person_duration_by_assistant(
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    try:
        persons = fetch_all_person_duration(current_user, db)
        return format_response(status.HTTP_200_OK, "Berhasil", persons)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))