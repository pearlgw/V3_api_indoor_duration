from sqlalchemy.orm import Session
from model.user import User
from utils.utils import hash_password

def seed_users(db: Session):
    users = [
        {
            "nim": "a11.1111.11111",
            "fullname": "admin",
            "address": "admin_address",
            "email": "admin@gmail.com",
            "hashed_password": hash_password("password"),
            "image": "y",
            "roles": "admin",
            "token": 1309
        },
        {
            "nim": "b11.1111.11111",
            "fullname": "user",
            "address": "user_address",
            "email": "user@gmail.com",
            "hashed_password": hash_password("password"),
            "image": "y",
            "roles": "user",
            "token": 1309
        },
    ]
    
    for user_data in users:
        user = User(**user_data)
        db.add(user)
    
    db.commit()
    print("Users seeded successfully.")
