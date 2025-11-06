


from src.models.auth import User
from src.schemas.auth import UserS
from src.repositories.mappers.base import DataMapper
from src.models.templates import Templates
from src.schemas.templates import NotificationSendS


class UserDataMapper(DataMapper):
    db_model = User
    schema = UserS
    
    
class TemplateDataMapper(DataMapper):
    db_model = Templates
    schema = NotificationSendS