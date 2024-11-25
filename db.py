from models.base import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = 'sqlite:///database.db'
engine = create_engine(DB_URL, echo=True)

Session = sessionmaker(engine)

def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)


if __name__ == "main":
    create_db_and_tables()
