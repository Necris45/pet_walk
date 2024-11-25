from contextlib import asynccontextmanager

import sqlalchemy
import uvicorn
from fastapi import FastAPI
from routers import ping, users
from models.users import User, Token


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#
#     yield


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(ping.router)
app.include_router(users.router)
