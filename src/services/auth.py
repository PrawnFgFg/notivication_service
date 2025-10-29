from fastapi import Response, Request
import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from asyncpg.exceptions import UniqueViolationError

from src.schemas.auth import UserCreateRequest, UserCreate, UserLoginIn
from src.services.base import BaseService
from src.config import settings
from src.exceptions import IncorrectPasswordException, UserNotFoundException, JWTTokenHasExpiredException


class AuthService(BaseService):
    
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
    
    
    def create_access_token(
        self, 
        payload: dict, 
        private_key: str = settings.auth_jwt.private_key_path.read_text(), 
        algorithm: str = settings.auth_jwt.algorithm
    ):
        to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        encoded_token = jwt.encode(to_encode, private_key, algorithm=algorithm)
        return encoded_token
        
    def decode_access_token(
        self, 
        token: str | bytes, 
        public_key: str = settings.auth_jwt.publick_key_path.read_text(), 
        algorithms: str = settings.auth_jwt.algorithm
    ):
        try:
            decoded_token = jwt.decode(token, public_key, algorithms=[algorithms])
        except ExpiredSignatureError:
            raise JWTTokenHasExpiredException
        
        return decoded_token
        
    
    def hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
    
    
    
    async def create_user(self, data_add: UserCreateRequest):
        
        hashed_password = self.hashed_password(data_add.password)
        
        data_schemas = UserCreate(hashed_password=hashed_password, **data_add.model_dump())
        
        if not self.verify_password(data_add.password, data_schemas.hashed_password):
            raise IncorrectPasswordException
        
        user = await self.db.users.create(data_schemas)
        await self.db.session.commit()
        return user
    
    
    async def login_in(
        self, 
        schema_login: UserLoginIn,
        response: Response,
        ):
        user = await self.db.users.get_one_by_filter(email=schema_login.email)
        if not user:
            raise UserNotFoundException
        if not self.verify_password(schema_login.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token(user.model_dump())
        response.set_cookie("access_token", access_token)
        return user
        
        
    async def get_me(self, user_id: int):
        me = await self.db.users.get_one_user_for_get_me(id=user_id)
        return me
    
    
    async def logout(self, response: Response):
        
        response.delete_cookie("access_token")
        return{"status": "Ok"}
    
    
    async def delete_me(self, response: Response, request: Request):
        access_token = request.cookies.get("access_token")
        payload_user = self.decode_access_token(access_token)
        current_user_id = payload_user.get("id")
        response.delete_cookie("access_token")
        await self.db.users.delete(id=current_user_id)
        await self.db.session.commit()
    
    
    
    async def change_name(self, schema_updt, user_id: int):
        await self.db.users.edit(id=user_id, schema_to_update=schema_updt)
        await self.db.session.commit()
    
        
        
    
    
        
        
        

    
        
        