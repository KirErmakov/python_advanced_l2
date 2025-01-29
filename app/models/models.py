from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import SQLModel, Field


class User(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str

class UserDataCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserDataUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str  | None = None
    avatar: HttpUrl | None = None

