import data
import json
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, paginate
from http import HTTPStatus
from models import *
from random import randint

app = FastAPI()
add_pagination(app)

users: list[UserData] = []


@app.get("/status", response_model=AppStatus,status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    if not users:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No users found"
        )
    return AppStatus(users=True)


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get("/api/users",response_model=Page[UserData], status_code=HTTPStatus.OK)
def get_users() -> list[UserData]:
    return  paginate(users)


@app.post("/api/users", response_model=CreatedUserData, status_code=HTTPStatus.CREATED)
def create_user(request_data: CreateUserRequest) -> CreatedUserData:
    new_id = randint(100, 250)
    date = data.timestamp

    return CreatedUserData(
        name=request_data.name,
        job=request_data.job,
        id=new_id,
        createdAt=date
    )


@app.post("/api/register", response_model=SuccessRegisterData, status_code=HTTPStatus.OK)
def register_user(user: User) ->SuccessRegisterData | JSONResponse:
    if user.email == data.register_user['email'] and user.password == data.register_user['password']:
        return SuccessRegisterData(id=4, token="QpwL5tke4Pnpja7X4")

    if not user.email:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing email or username"}
        )

    if not user.password:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing password"}
        )

    else:
        return JSONResponse(
            status_code=400,
            content={ "error": "Note: Only defined users succeed registration"}
        )


@app.put("/api/users/{user_id}", response_model=UpdatedUserData, status_code=HTTPStatus.OK)
def update_user(user_id: int, req_data: CreateUserRequest) -> UpdatedUserData | JSONResponse:
    user_ids = [5,7]
    date = data.timestamp
    if user_id not in user_ids:
        return JSONResponse(
            status_code=400,
            content={"error": "User ID does not exist"}
        )
    else:
        return UpdatedUserData(name=req_data.name, job=req_data.job, updatedAt=date)



@app.delete("/api/users/{user_id}")
def delete_user(user_id) -> Response:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return Response(status_code=HTTPStatus.NO_CONTENT)

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f"User with id {user_id} not found"
    )


if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        UserData.model_validate(user)

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
