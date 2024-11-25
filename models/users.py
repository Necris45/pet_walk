import sqlalchemy
# from sqlalchemy.dialects.postgresql import UUID
from db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, Session
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String(40), unique=True, index=True)
    name = Column(String(100))
    hashed_password = Column(String)
    room_number = Column(Integer)
    phone_number = Column(String(15))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Token(Base):

    __tablename__ = 'tokens'

    id = Column(Integer, autoincrement=True, primary_key=True)
    token = Column(String, nullable=False, index=True)
    expires = Column(DateTime)
    user_id = Column(ForeignKey("users.id"))

