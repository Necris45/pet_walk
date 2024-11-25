import hashlib
from datetime import datetime, timedelta
from sqlalchemy import and_

import models.users
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
    user = models.users.User(name=user.name,
                             email=user.email,
                             hashed_password=hash_password(user.password, user.name),
                             room_number=user.room_number,
                             phone_number=user.phone_number)
    await models.users.create_user(user)


async def get_user_by_email(email):
    await models.users.get_user_by_email(email)


async def get_user_by_token(token: str):
    await models.users.get_user_by_token(token)


async def create_user_token(user_id: int):
    """Create token for user with user_id."""
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    return await database.fetch_one(query)
