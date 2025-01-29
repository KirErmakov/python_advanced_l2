from fastapi import HTTPException
from sqlalchemy.testing.config import db_url
from sqlmodel import Session, select
from typing import Iterable, Type

from .engine import engine
from ..models.models import UserData


def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        return session.get(UserData, user_id)


def get_users() -> Iterable[UserData]:
    with Session(engine) as session:
        statement = select(UserData)
        return session.exec(statement).all()


def create_user(user: UserData) -> UserData:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user_id: int, user: UserData) -> UserData:
    with Session(engine) as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return  db_user





def delete_user(user_id):
    with Session(engine) as session:
        user = session.get(UserData, user_id)
        session.delete(user)
        session.commit()