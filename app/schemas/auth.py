from pydantic import BaseModel

class LoginIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterIn(BaseModel):
    username: str   
    full_name: str
    password: str
    role: str = "technician"   # default

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    class Config:
        orm_mode = True