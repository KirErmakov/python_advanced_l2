from pydantic import BaseModel, EmailStr, HttpUrl


class AppStatus(BaseModel):
    users: bool


class User(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class SupportInfo(BaseModel):
    url: str
    text: str


class SuccessRegisterData(BaseModel):
    id: int
    token: str


class CreateUserRequest(BaseModel):
    name: str
    job: str

class CreatedUserData(BaseModel):
    name: str
    job: str
    id: int
    createdAt: str


class UpdatedUserData(BaseModel):
    name: str
    job: str
    updatedAt: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportInfo
