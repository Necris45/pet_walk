import asyncio
import typer
from fastapi import FastAPI

from db import init_models
from routers import ping, users, appointments, orders

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
app.include_router(appointments.router)
app.include_router(orders.router)

if __name__ == "__main__":
    cli()
