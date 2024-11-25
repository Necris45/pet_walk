from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemas import users
from utils.dependecies import get_current_user
from utils.users import (new_user, get_user_by_email, validate_password, create_user_token,
                         add_pet_to_user, remove_pet_from_user)

router = APIRouter()


@router.post('/sign-up')
async def create_user(user: users.UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered.')
    return await new_user(session, user=user)


@router.post('/auth', response_model=users.TokenBase)
async def auth(format_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, email=format_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong e-mail or password')
    if not validate_password(password=format_data.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong e-mail or password')
    return await create_user_token(session, user_id=user.id, need_commit=True)


@router.get('/users/me', response_model=users.UserBase)
async def read_user(current_user: users.User = Depends(get_current_user)):
    return current_user


@router.post('/users/add_pet', response_model=users.PetsBase)
async def add_pets(pets: users.PetsBase, current_user: users.User = Depends(get_current_user),
                   session: AsyncSession = Depends(get_session)):
    if current_user.is_active:
        return await add_pet_to_user(session, pets, current_user)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User deactivated')


@router.post('/users/remove_pet', response_model=users.PetsBase)
async def remove_pets(pets: users.PetsBase, current_user: users.User = Depends(get_current_user),
                   session: AsyncSession = Depends(get_session)):
    if current_user.is_active:
        return await remove_pet_from_user(session, pets, current_user)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User deactivated')
