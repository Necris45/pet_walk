from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemas import users
from utils.dependecies import get_current_user
from utils.appointments import create_slots, date_with_slots, slots_on_date


router = APIRouter()


@router.post('/admin/generate_slots')
async def generate_free_slots(current_user: users.User = Depends(get_current_user),
                              session: AsyncSession = Depends(get_session),
                              date: str = None, days: int = 1):
    if current_user.is_admin:
        return await create_slots(session, current_user.id, date, days)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You not admin')


@router.get('/appointment_dates')
async def get_date_with_slots(current_user: users.User = Depends(get_current_user),
                              session: AsyncSession = Depends(get_session)):
    if current_user:
        return await date_with_slots(session)


@router.get('/appointment_slots_on_date')
async def get_slots_from_date(date: str, current_user: users.User = Depends(get_current_user),
                              session: AsyncSession = Depends(get_session)):
    if current_user:
        return await slots_on_date(session, date)
