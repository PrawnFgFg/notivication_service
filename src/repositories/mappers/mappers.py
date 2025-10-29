


from src.models.auth import User
from src.schemas.auth import UserS
from src.repositories.mappers.base import DataMapper


class UserDataMapper(DataMapper):
    db_model = User
    schema = UserS