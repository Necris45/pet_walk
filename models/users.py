import sqlalchemy
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, Session
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, select

from models.base import Base
from db import engine


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column()
    room_number: Mapped[int] = mapped_column(Integer())
    phone_number: Mapped[str] = mapped_column(String(15))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)


async def create_user(user: User) -> None:
    with Session() as session:
        try:
            session.add(user)
        except:
            session.rollback()
            raise
        else:
            session.commit()


async def get_user_by_email(email):
    with Session(engine) as session:
        stmt = select(User).where(email=email)
        db_object = session.scalars(stmt).one()
        return db_object


class Token(Base):
    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(), nullable=False, index=True)
    expires: Mapped[DateTime] = mapped_column(DateTime())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


async def get_user_by_token(token):
    with Session(engine) as session:
        stmt = (select(User).join(Token.user_id).where(Token.token == token))
        await session.scalars(stmt).one()
