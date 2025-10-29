from typing import Annotated
from fastapi import Depends, Request
from jwt.exceptions import DecodeError

from src.database import assync_session_maker
from src.utils.db_manager import DBManager
from src.services.auth import AuthService
from src.exceptions import JWTTokenHasExpiredHTTPException, JWTTokenHasExpiredException



def get_access_token(request: Request):
    access_token = request.cookies.get("access_token", None)
    return access_token

def get_current_user(token: str = Depends(get_access_token)):
    try:
        user = AuthService().decode_access_token(token)
    except JWTTokenHasExpiredException:
        raise JWTTokenHasExpiredHTTPException
    except DecodeError:
        raise JWTTokenHasExpiredHTTPException
    return user['id']



def dbmanager():
    return DBManager(session_factory=assync_session_maker)


async def get_db():
    async with dbmanager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
UserIdDep = Annotated[int, Depends(get_current_user)]