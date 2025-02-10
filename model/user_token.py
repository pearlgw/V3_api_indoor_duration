from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID
import uuid
from datetime import datetime
from typing import Optional

class UserToken(SQLModel, table=True):
    __tablename__="user_tokens"
    
    uid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_uid: Optional[uuid.UUID] = Field(default=None)
    token: str = Field(unique=True, nullable=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    expires_at: datetime = Field(nullable=False)