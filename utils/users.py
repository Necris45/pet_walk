import hashlib
import random
import string
import json
from datetime import datetime, timedelta
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import is_instance_of

from models.users import User, Token
from schemas.users import UserCreate
from db import get_session, engine
from utils.exceptions import DuplicatedEntryError


def get_random_string(length=12):
    """Return generated random string (salt)."""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """Hash password with salt."""
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """Validate password hash with db hash."""
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(session: AsyncSession, email: str):
    """Return user info by email."""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_token(session: AsyncSession, token: str):
    """Return user info by token."""
    result = await session.execute(select(Token).where(Token.token == token,
                                                       Token.expires > datetime.now()))
    order = result.scalars().first()
    user = await session.execute(select(User).where(User.id == order.user_id))
    return user.scalars().first()


async def create_user_token(session: AsyncSession, user_id: int, need_commit=False):
    new_token = Token(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
    session.add(new_token)
    result = await session.execute(select(Token).where(Token.user_id == user_id))
    if need_commit:
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise DuplicatedEntryError("this user already exist")
    return result.scalars().first()


async def new_user(session: AsyncSession, user: UserCreate):
    """Create new user."""
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    new_user = User(email=user.email, name=user.name, hashed_password=f"{salt}${hashed_password}",
                 room_number=user.room_number, phone_number=user.phone_number)
    session.add(new_user)
    result = await get_user_by_email(session, user.email)
    token = await create_user_token(session, result.id)
    try:
        await session.commit()
        token_dict = {"token": token.token, "expires": token.expires}
        return {**user.dict(), "id": result.id, "is_active": True, "token": token_dict}
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError("this user already exist")


async def add_pet_to_user(session: AsyncSession, new_pet, user):
    pet = {}
    pet['name'] = new_pet.name
    pet['species'] = new_pet.species
    pets = user.pets
    if pets:
        if pet in pets:
            raise DuplicatedEntryError("this pet already exist")
        if isinstance(pets, list) and len(pets) <= 5:
            pets.append(pet)
        elif isinstance(pets, list) and len(pets) >= 5:
            raise DuplicatedEntryError("you added too many pets")
        else:
            pets = []
            pets.append(pet)
            pets = json.dumps(pets)
    user.pets = pets
    try:
        await session.commit()
        return new_pet
    except:
        await session.rollback()
        raise DuplicatedEntryError("something going wrong, try again later")


async def remove_pet_from_user(session: AsyncSession, new_pet, user):
    pet = {}
    pet['name'] = new_pet.name
    pet['species'] = new_pet.species
    pets = user.pets
    if pets:
        if pet in pets:
            pets = [el for el in pets if el != pet]
        else:
            raise DuplicatedEntryError("you have not this pets")
    user.pets = pets
    try:
        await session.commit()
        return new_pet
    except:
        await session.rollback()
        raise DuplicatedEntryError("something going wrong, try again later")
