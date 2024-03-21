import asyncio

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database import get_session, SQLALCHEMY_DATABASE_URL
from src.books import models as books  # noqa
from src.Base import Base as BaseModel
from src.books.models import Book  # noqa F401

async_test_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

async_test_session = async_sessionmaker(async_test_engine, expire_on_commit=False, autoflush=False)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables() -> None:
    """Create tables in DB."""
    async with async_test_engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_test_engine.connect() as connection:
        async with async_test_session(bind=connection) as session:
            yield session
            await session.rollback()


@pytest.fixture(scope="function")
def override_get_async_session(db_session):
    async def _override_get_async_session():
        yield db_session

    return _override_get_async_session


@pytest.fixture(scope="function")
def test_app(override_get_async_session):
    from main import app

    app.dependency_overrides[get_session] = override_get_async_session

    return app


# создаем асинхронного клиента для ручек
@pytest_asyncio.fixture(scope="function")
async def async_client(test_app):
    async with httpx.AsyncClient(app=test_app, base_url="http://127.0.0.1:8000") as test_client:
        yield test_client