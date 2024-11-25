import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON


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
    pets = Column(JSON, default=list)


class Token(Base):

    __tablename__ = 'tokens'

    id = Column(Integer, autoincrement=True, primary_key=True)
    token = Column(UUID(as_uuid=False), server_default=sqlalchemy.text('uuid_generate_v4()'),
                   unique=True, nullable=False, index=True)
    expires = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id))
