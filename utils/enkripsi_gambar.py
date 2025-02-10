import uuid
import os
from pathlib import Path
from fastapi import HTTPException, UploadFile
from cryptography.fernet import Fernet

# Pastikan folder `image/` ada
UPLOAD_DIR = Path("image")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Ambil kunci enkripsi dari .env
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY tidak ditemukan di .env")

fernet = Fernet(ENCRYPTION_KEY.encode())

def save_encrypted_image(image: UploadFile) -> str:
    try:
        # Buat nama file acak dengan ekstensi `.enc`
        image_filename = f"{uuid.uuid4()}.enc"
        image_path = UPLOAD_DIR / image_filename

        # Baca data gambar
        img_data = image.file.read()
        encrypted_image = fernet.encrypt(img_data)  # Enkripsi gambar

        # Simpan gambar terenkripsi ke dalam file
        with open(image_path, "wb") as buffer:
            buffer.write(encrypted_image)

        return image_filename

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan gambar: {str(e)}")

def decrypt_image(image_filename: str, fernet: Fernet):
    image_path = UPLOAD_DIR / image_filename

    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Gambar tidak ditemukan")

    try:
        with open(image_path, "rb") as enc_file:
            encrypted_data = enc_file.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mendekripsi gambar: {str(e)}")
