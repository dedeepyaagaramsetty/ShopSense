from pydantic import BaseModel, EmailStr

class VendorCreate(BaseModel):
    business_name: str
    owner_name: str
    email: EmailStr
    phone: str
    password: str


class VendorResponse(BaseModel):
    id: int
    business_name: str
    owner_name: str
    email: str
    phone: str
    status: str

    class Config:
        from_attributes = True

class VendorLogin(BaseModel):
    email: EmailStr
    password: str