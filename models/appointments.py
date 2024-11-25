from db import Base
from sqlalchemy import Column, Integer, Boolean, Date, Time, ForeignKey
from models.users import User


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    date = Column(Date)
    time = Column(Time)
    is_free = Column(Boolean, default=True)
    staff_id = Column(Integer, ForeignKey(User.id))
