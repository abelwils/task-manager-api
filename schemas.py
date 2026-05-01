from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str


class TaskCreate(BaseModel):
    title: str
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool
    priority: str
    due_date: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True