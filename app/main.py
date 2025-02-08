import logging
from contextlib import asynccontextmanager

import dotenv


dotenv.load_dotenv()

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import users, status
from app.db.engine import create_db_and_tables



@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.warning('On startup')
    create_db_and_tables()
    yield
    logging.warning('On shutdown')

app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
