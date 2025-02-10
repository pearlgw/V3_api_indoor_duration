from fastapi import APIRouter, Depends, HTTPException, Response
from utils.utils import get_current_user
from utils.enkripsi_gambar import decrypt_image
from cryptography.fernet import Fernet
import os
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(ENCRYPTION_KEY)

encrypted_image = APIRouter()

@encrypted_image.get("/{image_filename}")
def decrypt_display_image(image_filename: str, cur_user: dict = Depends(get_current_user)):
    if cur_user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Akses hanya untuk admin")
        
    if not image_filename.endswith(".enc"):
        raise HTTPException(status_code=400, detail="Format file tidak valid")
    
    decrypted_image = decrypt_image(image_filename, fernet)
    
    return Response(content=decrypted_image, media_type="image/jpeg")