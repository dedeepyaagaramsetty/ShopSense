from pydantic import BaseModel
from datetime import datetime


class CustomerCreate(BaseModel):

    full_name: str
    email: str
    phone: str
    password: str
    address: str


class CustomerLogin(BaseModel):

    email: str
    password: str


class CustomerResponse(BaseModel):

    id: int
    full_name: str
    email: str
    phone: str
    address: str
    created_at: datetime

    class Config:
        from_attributes = True