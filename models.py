from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    userId: str
    username: str
    password: str
    profile_image_url: Optional[str] = None

class Habit(BaseModel):
    habitId: str
    userId: str
    name: str
    color: Optional[str] = '#FFFFFF'
    created_at: datetime
    entries: List[dict] = []

class HabitEntry(BaseModel):
    date: datetime
    value: int