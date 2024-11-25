import asyncio
import typer
from fastapi import FastAPI
from datetime import datetime
from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.exc import IntegrityError
from utils.exceptions import DuplicatedEntryError
from db import init_models
from db import get_session
from routers import ping, users

app = FastAPI()
cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(ping.router)
app.include_router(users.router)

if __name__ == "__main__":
    cli()
