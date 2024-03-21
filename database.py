from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from src.sellers.models import metadata as sellers_metadata
from src.books.models import metadata as books_metadata
from src.Base import Base
SQLALCHEMY_DATABASE_URL = ("postgresql+psycopg2://login:password@localhost:5432/demo")



engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
session_maker = sessionmaker(engine, class_=Session, expire_on_commit=False)
print(sellers_metadata)
# sellers_metadata.create_all(engine)
# books_metadata.create_all(engine)

Base.metadata.create_all(engine)


def get_session():
    with session_maker() as session:
        yield session
