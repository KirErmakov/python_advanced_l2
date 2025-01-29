from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from http import HTTPStatus
from typing import Iterable

from app.db import users
from app.models.models import *


router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return user


@router.get("/", response_model=Page[UserData], status_code=HTTPStatus.OK)
def get_users() -> Iterable[UserData]:
    return  paginate(users.get_users())


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: UserData) -> UserData:
    UserDataCreate.model_validate(user.model_dump())

    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserData) -> UserData | None:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    UserDataUpdate.model_validate(user.model_dump())
    updated_user = users.update_user(user_id, user)
    return updated_user



@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users.delete_user(user_id)
    return {'message': 'User deleted'}

