from dotenv import load_dotenv
from sqlmodel import Session
from model.person_duration import PersonDuration, DetailPersonDuration
from sqlalchemy import desc

load_dotenv()

def fetch_all_person_duration(current_user, db: Session):
    fullname = current_user.get("fullname")
    persons = db.query(PersonDuration).filter(PersonDuration.name == fullname).order_by(desc(PersonDuration.created_at)).all()
    return persons