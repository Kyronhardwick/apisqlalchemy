from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentInDB(StudentBase):
    id: int
    class Config:
        orm_mode = True