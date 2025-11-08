from sqlalchemy.ext.asyncio import AsyncSession


from src.database import assync_session_maker
from src.repositories.auth import UserRepository
from src.repositories.notifications import NotificationRepository
from src.repositories.notification_logs import NotificationLogRepository

class DBManager:
    
    def __init__(self, session_factory: AsyncSession = assync_session_maker):
        self.session_factory = session_factory
        
    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.users = UserRepository(self.session)
        self.notifications = NotificationRepository(self.session)
        self.notification_logs = NotificationLogRepository(self.session)
        
        return self
        
        
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()
        
        
    async def commit(self,):
        return await self.session.commit()
    

    

