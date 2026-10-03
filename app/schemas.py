from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    course: str = Field(min_length=2, max_length=100)
    year: int = Field(ge=1, le=6)


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str
    year: int

    class Config:
        from_attributes = True