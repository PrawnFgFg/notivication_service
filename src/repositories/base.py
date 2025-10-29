from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Sequence

from src.repositories.mappers.base import DataMapper
from src.exceptions import ObjectAlreadyExistException
from src.schemas.auth import UserS


class BaseRepository:
    model = None
    mapper: DataMapper = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, schema_add):
        try:
            stmt_add = insert(self.model).values(**schema_add.model_dump()).returning(self.model)
            res = await self.session.execute(stmt_add)
            return res.scalars().one()
        except IntegrityError:
            raise ObjectAlreadyExistException
        
    async def create_bulk(self, data_list: Sequence[BaseModel]):
        stmt_add_bulk = insert(self.model).values([item.model_dump() for item in data_list])
        await self.session.execute(stmt_add_bulk)
    
    
    
    async def get_one_by_filter(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalar_one()
        return self.mapper.map_to_domain_entity(model)
    
    
    
    async def edit(self, schema_to_update: BaseModel, exclude_unset: bool = False,  **filter_by):
        stmt_edit = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**schema_to_update.model_dump(exclude_unset=exclude_unset))
            )
        await self.session.execute(stmt_edit) 
         
        
    
    
    
    
    async def delete(self, **filter_by):
        stmt_del = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt_del)
        