from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class Member(BaseModel):
    name: str
    email: EmailStr

class EventCreate(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    members: List[Member]