


from src.repositories.base import BaseRepository
from src.models.templates import Templates
from src.repositories.mappers.mappers import TemplateDataMapper


class NotificationRepository(BaseRepository):
    model = Templates
    mapper = TemplateDataMapper