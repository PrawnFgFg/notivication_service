from typing import Type, TypeVar
from pydantic import BaseModel


from src.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel) 


class DataMapper:
    db_model: Type[Base]
    schema: Type[SchemaType]
    
    
    @classmethod
    def map_to_domain_entity(cls, db_model):
        return cls.schema.model_validate(db_model, from_attributes=True)
    
    
    @classmethod
    def map_to_presistence_entity(cls, schema):
        return cls.db_model(**schema.model_dump())
    