import threading
import time
from fastapi import FastAPI
from db.database import engine
from sqlmodel import SQLModel, select, Session
from routes.admin import admin_router
from routes.auth import auth_router
from routes.log import log_router
from routes.person_duration import person_duration_router
from routes.assistant import assistant_router
from routes.encrypted_images import encrypted_image
from model.user_token import UserToken
from datetime import datetime

version = "3"
app = FastAPI(
    title="Indoor Duration App Reborn",
    description=f"Api Indoor Duration Reborn version {version}",
    version=version
)

SQLModel.metadata.create_all(engine)

def cleanup_expired_tokens():
    """Fungsi untuk menghapus token yang sudah kedaluwarsa setiap 1 menit."""
    while True:
        with Session(engine) as session:
            query = select(UserToken).where(UserToken.expires_at < datetime.now())
            expired_tokens = session.exec(query).all()
            
            for token in expired_tokens:
                session.delete(token)
            
            session.commit()
        
        time.sleep(60)

def start_cleanup_thread():
    thread = threading.Thread(target=cleanup_expired_tokens, daemon=True)
    thread.start()

@app.on_event("startup")
def startup_event():
    start_cleanup_thread()

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(admin_router, prefix=f"/api/{version}/admin", tags=["Admin"])
app.include_router(encrypted_image, prefix=f"/api/{version}/image", tags=["View Encrypted Images"])
app.include_router(person_duration_router, prefix=f"/api/{version}/person_duration", tags=["Person Duration"])
app.include_router(assistant_router, prefix=f"/api/{version}/assistant", tags=["Assistant"])
app.include_router(log_router, prefix=f"/api/{version}/logs", tags=["Logs"])