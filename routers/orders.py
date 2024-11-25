from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from schemas import users
from utils.dependecies import get_current_user
from utils.appointments import change_appointment_status
from utils.users import check_pet
from schemas import orders
from utils.orders import create_order, get_orders_on_day


router = APIRouter()


@router.post('/orders/create')
async def order_create(order: orders.OrdersCreate = Depends(),
                       current_user: users.User = Depends(get_current_user),
                       session: AsyncSession = Depends(get_session)):
    if current_user:
        slot = await change_appointment_status(session, order.date, order.time, order.staff_id)
        pet = await check_pet(session, order.pet_name, order.pet_species, current_user)
        return await create_order(session, slot, pet, current_user)



@router.get('/orders_on_day')
async def order_create(date: str, current_user: users.User = Depends(get_current_user),
                       session: AsyncSession = Depends(get_session)):
    if current_user.is_admin:
        return await get_orders_on_day(session, date, current_user.id)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You not admin')
