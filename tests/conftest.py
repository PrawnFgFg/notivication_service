import pytest
# import json
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.config import settings
from src.utils.db_manager import DBManager
from src.main import app
# from src.schemas.auth import UserCreateRequest
# from src.services.auth import AuthService

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"
    
    
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope="function", autouse=False)
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    # with open("tests/mock_auth.json", "r", encoding="utf-8") as file_auth:
    #     users = json.load(file_auth)
        
    # user_data = [UserCreateRequest(AuthService().hashed_password(UserCreateRequest.password)).model_validate(user) for user in users]
        
    # async with DBManager(session_factory=async_session_maker_null_pool) as db_:
    #     # await db_.users.create_bulk(user_data)
    #     await AuthService(db_).create_user(user_data)
    #     await db_.commit()



@pytest.fixture(scope="session", autouse=False)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
        
@pytest.fixture(scope="session")
async def register_user(ac: AsyncClient, setup_database):
    resp_register = await ac.post(
        "/auth/register",
        json={
            "email": "main_user@example.com",
            "password": "string123",
            "nickname": "main_user"
        }
    )
    
    assert resp_register.status_code == 200


@pytest.fixture(scope="session")    
async def authenticated_user(ac: AsyncClient, register_user):
    login_resp = await ac.post(
        "/auth/login",
        json={
            "email": "main_user@example.com",
            "password": "string123"
        }
    )
    
    assert login_resp.status_code == 200
    assert login_resp.cookies.get("access_token")
    yield ac
    



    