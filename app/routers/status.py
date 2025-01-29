from fastapi import APIRouter, HTTPException
from http import HTTPStatus

from app.db.engine import check_db_availability
from app.models.AppStatus import AppStatus

router = APIRouter()

@router.get("/status", response_model=AppStatus,status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    return AppStatus(database=check_db_availability())