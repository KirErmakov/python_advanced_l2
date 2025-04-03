from typing import Type
from pydantic import BaseModel, ValidationError
from requests import Response


def parse_response(response: Response, model: Type[BaseModel]) -> BaseModel:
    response.raise_for_status()
    try:
        return model.model_validate(response.json())
    except ValidationError as e:
        raise ValueError(f"Invalid response data: {e}")
