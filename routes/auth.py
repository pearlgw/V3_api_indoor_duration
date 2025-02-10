from fastapi import APIRouter, Depends, status, HTTPException
from schema.admin import LoginRequest
from sqlalchemy.orm import Session
from db.database import get_db
from service.auth import login_service, logout_service
from utils.utils import get_current_user, format_response
from middleware.verify_token import verify_token_validity

auth_router = APIRouter()

@auth_router.post("/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = login_service(login_data, db)
        return format_response(status.HTTP_200_OK, "Login berhasil", token)
    except HTTPException as e:
        return format_response(e.status_code, "Login gagal", error=str(e.detail))
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Login gagal", error=str(e))

@auth_router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return format_response(status.HTTP_200_OK, "Berhasil", current_user)

@auth_router.post("/logout")
def logout_user(authorization: str = Depends(verify_token_validity), db: Session = Depends(get_db)):
    try:
        token = authorization.token
        message = logout_service(token, db)

        return format_response(status.HTTP_200_OK, message)
    
    except HTTPException as e:
        return format_response(e.status_code, "Logout gagal", error=str(e.detail))
    
    except Exception as e:
        return format_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Logout gagal", error=str(e))