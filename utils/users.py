import hashlib
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import *
from schemas.users import UserCreate


def hash_password(password: str, name: str = None):
    """Hash password with salt."""
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), name.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """Validate password hash with db hash."""
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def new_user(user: UserCreate):
    """Create new user."""
    token = hash_password(user.password, user.name)
    new_user = User(name=user.name,
                    email=user.email,
                    hashed_password=token,
                    room_number=user.room_number,
                    phone_number=user.phone_number)
    session.add(new_user)
    user_result = await session.
    token = await create_user_token(user_result.id, token)
    return {**user.dict(), "id": user_result.id, "is_active": True, "token": token}


async def get_user_by_email(email):
    await models.users.get_user_by_email(email)


async def get_user_by_token(token: str):
    await models.users.get_user_by_token(token)


async def create_user_token(user_id: int, token: str):
    token = models.users.Token(token=token,
                               expires=datetime.now() + timedelta(weeks=2),
                               user_id=user_id)
    await models.users.create_token(token)
