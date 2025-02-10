from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select
from db.database import get_db
from service.person_duration import create_person_duration_service, create_detail_person_duration_service, fetch_all_person_duration, fetch_get_detail_person_duration, update_end_time_detail_indoor_duration
from utils.utils import get_current_user, format_response
from model.person_duration import PersonDuration, DetailPersonDuration
from uuid import UUID
from datetime import datetime
from schema.person_duration import UpdateEndTimeRequest

person_duration_router = APIRouter()

# pakai ini ketika untuk menghasilkan semua data relasi
# @person_duration_router.get("/")
# def get_all_person_duration(
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     if current_user["role"] != "admin":
#         raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
#     try:
#         # Ambil semua data PersonDuration
#         query = select(PersonDuration)
#         result = db.execute(query)
#         person_durations = result.scalars().all()

#         # Ambil detail secara manual berdasarkan uid
#         response_data = []
#         for pd in person_durations:
#             detail_query = select(DetailPersonDuration).where(DetailPersonDuration.person_duration_uid == pd.uid)
#             detail_result = db.execute(detail_query)
#             details = detail_result.scalars().all()

#             response_data.append({
#                 "uid": pd.uid,
#                 "name": pd.name,
#                 "total_duration": pd.total_duration,
#                 "status": pd.status,
#                 "created_at": pd.created_at,
#                 "details": [detail.model_dump() for detail in details]
#             })

#         return format_response(status.HTTP_200_OK, "Berhasil", response_data)
    
#     except Exception as e:
#         return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))

@person_duration_router.get("/")
def get_all_person_duration(
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user)
):
    # if current_user["role"] != "admin":
    #     raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
    try:
        # Ambil semua data PersonDuration
        person_durations = fetch_all_person_duration(db)
        return format_response(status.HTTP_200_OK, "Berhasil", person_durations)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))
    
@person_duration_router.get("/detail/{uid_person_duration}")
def get_detail_person_duration(
    uid_person_duration: UUID, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    # if current_user["role"] != "admin":
    #     raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
    try:
        details = fetch_get_detail_person_duration(uid_person_duration, db, current_user)
        return format_response(
            status.HTTP_200_OK, 
            "Berhasil", 
            details
        )
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))
        
@person_duration_router.post("/create")
def create_person_duration(
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Cek apakah user yang mengakses adalah admin
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
    try:
        new_person_duration = create_person_duration_service(
            data_name=name,
            db=db,
            current_user=current_user
        )
        return format_response(status.HTTP_201_CREATED, "Data berhasil dibuat", new_person_duration)
    
    except HTTPException as e:
        return format_response(e.status_code, "Data gagal dibuat", error=e.detail)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))
    
@person_duration_router.post("/detail/create")
def create_detail_person_duration(
    nim: str = Form(...),
    name: str = Form(...),
    name_track_id: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Cek apakah user yang mengakses adalah admin
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
    
    try:
        new_detail = create_detail_person_duration_service(
            data_nim=nim,
            data_name=name,
            data_name_track_id=name_track_id,
            data_image=image,
            db=db,
            current_user=current_user
        )
        return format_response(status.HTTP_201_CREATED, "Data berhasil dibuat", new_detail)
    
    except HTTPException as e:
        return format_response(e.status_code, "Data gagal dibuat", error=e.detail)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))
    
@person_duration_router.patch("/detail/{track_name_id}")
def update_end_time(
    track_name_id: str, 
    request: UpdateEndTimeRequest,
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Akses hanya untuk admin")

    try:
        update_detail_end_time = update_end_time_detail_indoor_duration(track_name_id, request, db, current_user)
        return format_response(status.HTTP_200_OK, "Data berhasil diupdate", update_detail_end_time)
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Data gagal dibuat", error=str(e))