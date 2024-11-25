from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time

from models.users import User


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    room_number = Column(Integer)
    pet_name = Column(String)
    pet_species = Column(String)
    date = Column(Date)
    time = Column(Time)
    staff_id = Column(Integer, ForeignKey(User.id))
    user_id = Column(Integer, ForeignKey(User.id))
