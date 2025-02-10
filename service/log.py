from sqlmodel import Session, select
from model.log import Log
from model.log import Log

def format_all_logs(db: Session, fullname: str, action: str):
    new_log = Log(name=fullname, action=action)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_all_logs(db: Session):
    query = select(Log)
    result = db.execute(query)
    logs = result.scalars().all()
    return logs