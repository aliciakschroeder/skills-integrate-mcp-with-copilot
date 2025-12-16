from typing import List, Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class Activity(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: str
    schedule: str
    max_participants: int
    participants: List[str] = Field(sa_column=Column(JSON), default=[])
