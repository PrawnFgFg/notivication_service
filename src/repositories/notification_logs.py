


from src.repositories.base import BaseRepository
from src.models.notification_logs import NotificationLogs
from src.repositories.mappers.mappers import NotificationLogDataMapper


class NotificationLogRepository(BaseRepository):
    model = NotificationLogs
    mapper = NotificationLogDataMapper
    
    
   
    