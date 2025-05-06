from pydantic import BaseModel 

class UseIn(BaseModel):
    username: int
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    is_on_duty: bool

    class Config:
        orm_mode = True
