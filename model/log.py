from sqlmodel import SQLModel, Field, Column, Text
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB

class Log(SQLModel, table=True):
    __tablename__="logs"
    
    uid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    action: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))