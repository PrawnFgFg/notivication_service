from sqlalchemy import select

from src.models.auth import User
from src.repositories.base import BaseRepository
from src.schemas.auth import UserSGetMe
from src.repositories.mappers.mappers import UserDataMapper


class UserRepository(BaseRepository):
    model = User
    mapper = UserDataMapper
    
    
    
    async def get_one_user_for_get_me(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        user = res.scalar_one_or_none()
        if user is not None:
            return UserSGetMe.model_validate(user, from_attributes=True)
        return None
    
    
    
    
    