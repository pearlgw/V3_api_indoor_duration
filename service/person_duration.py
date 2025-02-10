from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlmodel import Session, select
from model.person_duration import PersonDuration, DetailPersonDuration
from utils.enkripsi_gambar import save_encrypted_image
from utils.utils import format_response, convert_seconds_to_time
import re
from datetime import datetime
from sqlalchemy import func
from uuid import UUID
from .log import format_all_logs

load_dotenv()

def fetch_all_person_duration(db: Session):
    query = select(PersonDuration)
    result = db.execute(query)
    person_durations = result.scalars().all()
    return person_durations

def fetch_get_detail_person_duration(uid_person: UUID, db: Session, current_user: dict):
    person_duration = db.get(PersonDuration, uid_person)
    if not person_duration:
        raise HTTPException(status_code=404, detail="Person duration tidak ditemukan")

    detail_query = select(DetailPersonDuration).where(DetailPersonDuration.person_duration_uid == uid_person)
    detail_result = db.execute(detail_query)
    details = detail_result.scalars().all()

    if not details:
        return format_response(status.HTTP_200_OK, "Tidak ada detail yang ditemukan", [])
    
    if current_user['role'] != "admin":
        for detail in details:
            delattr(detail, "labeled_image")
            delattr(detail, "person_duration_uid")
            delattr(detail, "uid")
            delattr(detail, "name_track_id")
    
    return details

def create_person_duration_service(data_name, db: Session, current_user: dict):
    cleaned_name = re.sub(r'\d+$', '', data_name)
    
    today = datetime.today().date()
    
    existing_entry = db.exec(
        select(PersonDuration).where(
            PersonDuration.name == cleaned_name,
            func.date(PersonDuration.created_at) == today
        )
    ).first()
    
    if existing_entry:
        raise HTTPException(status_code=400, detail="Maaf, data ini sudah ada untuk hari ini")
    
    new_person_duration = PersonDuration(
        name=cleaned_name
    )
    
    log_fullname = current_user.get("fullname")
    action_data = f"{log_fullname} created data person duration: {new_person_duration.dict()}"
    format_all_logs(db, log_fullname, action_data)
    
    db.add(new_person_duration)
    db.commit()
    db.refresh(new_person_duration)
    return new_person_duration

def create_detail_person_duration_service(data_nim, data_name, data_name_track_id, data_image, db: Session, current_user):
    cleaned_name = re.sub(r'\d+$', '', data_name_track_id)
    
    today = datetime.today().date()
    
    person_duration = db.exec(
        select(PersonDuration).where(
            PersonDuration.name == cleaned_name,
            func.date(PersonDuration.created_at) == today
        )
    ).first()

    if not person_duration:
        raise HTTPException(status_code=404, detail="Person Duration tidak ditemukan untuk hari ini")
    
    try:
        image_path = save_encrypted_image(data_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan gambar: {str(e)}")
    
    new_detail_indoor = DetailPersonDuration(
        person_duration_uid=person_duration.uid,
        nim=data_nim,
        name=data_name,
        name_track_id=data_name_track_id,
        labeled_image=image_path
    )
    
    person_duration = db.query(PersonDuration).filter(PersonDuration.uid == new_detail_indoor.person_duration_uid).first()
    
    if not person_duration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data tidak ditemukan")
    
    person_duration.status = "indoor"
    
    log_fullname = current_user.get("fullname")
    action_data = f"{log_fullname} created data detail person duration: {new_detail_indoor.dict()}"
    format_all_logs(db, log_fullname, action_data)
    
    db.add(new_detail_indoor)
    db.commit()
    db.refresh(new_detail_indoor)
    return new_detail_indoor

def update_end_time_detail_indoor_duration(track_name_id, request, db:Session, current_user: dict):
    detail_person_duration = db.query(DetailPersonDuration).filter(DetailPersonDuration.name_track_id == track_name_id).first()

    if not detail_person_duration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data tidak ditemukan")

    detail_person_duration.end_time = request.end_time
    
    person_duration = db.query(PersonDuration).filter(PersonDuration.uid == detail_person_duration.person_duration_uid).first()
    
    if not person_duration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data tidak ditemukan")
    
    person_duration.status = "outdoor"
    
    start_time = detail_person_duration.start_time
    end_time = detail_person_duration.end_time
    
    if start_time and end_time:
        duration = (end_time - start_time).total_seconds()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start time atau End time tidak valid")

    if person_duration.total_duration:
        total_duration_seconds = (datetime.combine(datetime.min, person_duration.total_duration) - datetime.min).total_seconds()
    else:
        total_duration_seconds = 0

    total_duration_seconds += duration

    # Konversi total detik kembali ke format time
    formatted_duration = convert_seconds_to_time(total_duration_seconds)

    person_duration.total_duration = formatted_duration
    
    log_fullname = current_user.get("fullname")
    action_data = f"{log_fullname} updated data end_time detail person duration: {detail_person_duration.dict()}"
    format_all_logs(db, log_fullname, action_data)

    db.commit()
    return {
        "end_time": detail_person_duration.end_time,
        "total_duration": formatted_duration
    }