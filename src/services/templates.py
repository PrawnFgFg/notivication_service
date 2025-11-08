from sqlalchemy.exc import NoResultFound
from datetime import date


from src.services.base import BaseService
from src.models.templates import Templates
from src.repositories.mappers.mappers import TemplateDataMapper
from src.schemas.templates import NotificationSendRequestS
from src.tasks.tasks import notification_task
from src.exceptions import NotFullBodyRequest
from src.exceptions import InvalidTemplateException
from src.schemas.notification_logs import NotificationLogS

from src.config import settings

class TemplateService(BaseService):
    model = Templates
    mapper = TemplateDataMapper
    
    
    async def send_notification(
        self,
        request: NotificationSendRequestS
    ):
        try:
            template = await self.db.notifications.get_one_by_filter(template_key=request.template_key)
        except NoResultFound:
            raise InvalidTemplateException
            
        request_data = request.model_dump()
        template_data = template.model_dump()
        self.verify_data(request_data)
        
        data_log = NotificationLogS(
            user_id=request_data["user_id"],
            template_key=request_data['template_key'],
            body=request_data["body"],
            channels=request_data["channels"],
            status="queued",
            sent_at=date.today()
        )
        
        log = await self.db.notification_logs.create(data_log)
        await self.db.commit()
        log_id = log.id
        print(log_id)

        notification_task.delay(template_data, request_data, log_id)
        
        return {"status": "Уведомление отправлено"}
    
    
    def verify_data(self, request_data: dict):
        body = request_data.get("body", None)

        required_body: list[str] = ["username", "order_id", "user_email", "telegram_id", "delivery_date"]
        for body_one in required_body:
            if body_one not in body:
                raise NotFullBodyRequest(f"Необходимо указать в body {body_one}")
        

        
        
    


