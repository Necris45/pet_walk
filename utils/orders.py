from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models.orders import Order
from utils.exceptions import DuplicatedEntryError


async def create_order(session: AsyncSession, slot, pet, current_user):
    """Create new order."""
    new_order = Order(room_number=current_user.room_number,
                      pet_name = pet['name'],
                      pet_species = pet['species'],
                      date = slot.date,
                      time = slot.time,
                      staff_id = slot.staff_id,
                      user_id = current_user.id)
    session.add(new_order)
    try:
        await session.commit()
        return {"answer": "you order created"}
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError("Order not created")


async def get_orders_on_day(session: AsyncSession, date:str, staff_id: int):
    search_on_date = datetime.strptime(date, "%Y-%m-%d")
    result = await session.execute(select(Order).where(Order.date == search_on_date.date(),
                                                       Order.staff_id == staff_id))
    finding_orders = result.scalars().all()
    return [row for row in finding_orders]
