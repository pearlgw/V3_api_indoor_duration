from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.orm import relationship  # Tambahkan import ini
from uuid import UUID
import uuid
from datetime import datetime, time
from typing import List, Optional

class PersonDuration(SQLModel, table=True):
    __tablename__= "person_durations"
    
    uid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    total_duration: time = Field(sa_column=Column(pg.TIME, nullable=True))
    status: str = Field(sa_column=Column(pg.VARCHAR, nullable=True))
    created_at: datetime = Field(sa_column=Column(default=datetime.now))
    
    details: List["DetailPersonDuration"] = Relationship(
        back_populates="person_duration",
    )

class DetailPersonDuration(SQLModel, table=True):
    __tablename__= "detail_person_durations"
    
    uid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    person_duration_uid: UUID = Field(foreign_key="person_durations.uid")
    labeled_image: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    nim: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    name_track_id: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    start_time: datetime = Field(sa_column=Column(default=datetime.now))
    end_time: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=True))
    
    person_duration: Optional["PersonDuration"] = Relationship(
        back_populates="details",
    )