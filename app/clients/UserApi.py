from http import HTTPStatus
from typing import Optional
from pydantic import ValidationError, BaseModel

from app.models.models import UserData, UserDataCreate, UserDataUpdate
from utils.base_session import BaseSession
from utils.response_parser import parse_response


class UserApi:
    def __init__(self, session: BaseSession):
        self.session = session

    def get_user(self, user_id: int) -> BaseModel:
        response = self.session.get(f"/api/users/{user_id}")
        response.raise_for_status()
        return parse_response(response, UserData)

    def get_users(self) -> list[UserData]:
        response = self.session.get("/api/users/")
        response.raise_for_status()

        try:
            return [UserData.model_validate(user) for user in response.json().get("items", [])]
        except ValidationError as e:
            raise ValueError(f"Invalid user list data: {e}")

    def create_user(self, user_data: UserDataCreate) -> BaseModel:
        response = self.session.post(
            "/api/users/",
            json=user_data.model_dump(mode='json')
        )
        response.raise_for_status()
        return parse_response(response, UserData)

    def update_user(self, user_id: int, user_data: UserDataUpdate) -> Optional[BaseModel]:
        response = self.session.patch(
            f"/api/users/{user_id}",
            json=user_data.model_dump(exclude_unset=True)
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            response.raise_for_status()

        return parse_response(response, UserData)

    def delete_user(self, user_id: int) -> bool:
        response = self.session.delete(f"/api/users/{user_id}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            response.raise_for_status()
        response.raise_for_status()
        return response.status_code == HTTPStatus.OK

    def get_status(self):
        return self.session.get("/status")
