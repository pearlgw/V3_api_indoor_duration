from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID
import uuid
import random
from datetime import datetime

def random_token_user():
    token = random.randint(1000, 9999)
    return token

class User(SQLModel, table=True):
    __tablename__="users"
    
    uid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nim: str = Field(max_length=16, sa_column=Column(nullable=False))
    fullname: str = Field(max_length=50, sa_column=Column(nullable=False))
    address: str = Field(max_length=50, sa_column=Column(nullable=False))
    email: str = Field(max_length=50, sa_column=Column(nullable=False))
    hashed_password: str = Field(sa_column=Column(
        nullable=False
    ))
    image: str = Field(sa_column=Column(
        nullable=False
    ))
    roles: str = Field(sa_column=Column(
        default="user"
    ))
    is_verified: bool = Field(sa_column=Column(nullable=True))
    token: int = Field(max_length=5, sa_column=Column(default=random_token_user))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    