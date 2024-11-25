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
from models.appointments import Appointment
from schemas.users import UserCreate
from db import get_session, engine
from utils.exceptions import DuplicatedEntryError


async def appointment_on_date_is_exist(session: AsyncSession, date, staff_id):
    result = await session.execute(select(Appointment.date)
                                   .where(Appointment.date == date,
                                          Appointment.staff_id == staff_id))
    return result.scalars().first()


async def create_slots(session: AsyncSession, user_id, create_on_date: str = None, days: int = 1):
    """
    :return: date of all days with free slots
    """
    new_appointments_count = 0
    if create_on_date is None:
        create_on_date = datetime.now()
        create_on_date = create_on_date + timedelta(days=1)
    else:
        create_on_date = datetime.strptime(create_on_date, "%Y-%m-%d")
    for day in range(1, days + 1):
        if (create_on_date.date() <= datetime.now().date() or
                await appointment_on_date_is_exist(session, create_on_date.date(), user_id)):
            create_on_date = create_on_date + timedelta(days=1)
            continue
        else:
            create_on_date = create_on_date.strftime("%Y-%m-%d")
            create_on_date += ' 07:00'
            create_on_date = datetime.strptime(create_on_date, "%Y-%m-%d %H:%M")
        while create_on_date.hour < 23 or (create_on_date.hour == 23 and create_on_date.minute < 30):
            new_appointments = Appointment(date=create_on_date.date(),time = create_on_date.time(),
                                                staff_id = user_id)
            create_on_date = create_on_date + timedelta(minutes=30)
            session.add(new_appointments)
            try:
                await session.commit()
                new_appointments_count += 1
            except:
                await session.rollback()
        create_on_date = create_on_date + timedelta(days=1)
    return {"answer": f"{new_appointments_count} slots created"}


async def date_with_slots(session: AsyncSession):
    """
    :return: date of all days with free slots
    """
    result = await session.execute(select(Appointment.date)
                                   .where(Appointment.is_free == True,
                                          Appointment.date > datetime.now()).distinct())
    find_dates = result.scalars().all()
    return [row.strftime("%Y-%m-%d") for row in find_dates]


async def slots_on_date(session: AsyncSession, date: str):
    result = await session.execute(select(Appointment.time, Appointment.staff_id)
                                   .where(Appointment.is_free == True,
                                          Appointment.date == datetime.strptime(date, "%Y-%m-%d")))
    find_time = result.scalars().all()
    return find_time
