from fastapi import APIRouter, Body




from config import settings
from src.services.templates import TemplateService
from src.api.dependencies import DBDep
from src.schemas.templates import NotificationSendRequestS
from src.exceptions import NotFullBodyRequest, NotFullBodyRequestHTTPException, InvalidTemplateHTTPException, \
    InvalidTemplateException


router = APIRouter(prefix="/notifications", tags=["Уведомления"])



@router.post("/send", summary="Отправить уведомление")
async def send_notification(
    db: DBDep,
    request: NotificationSendRequestS = Body(
        openapi_examples={
            "1": {
                "summary": "Новый заказ",
                "value": {
                    "template_key": "new_order",
                    "user_id": 23,
                    "body": {
                        "username": "Анна",
                        "order_id": 2345,
                        "user_email": "exampleforvvv@mail.ru",
                        "telegram_id": settings.MY_CHAT_ID,
                        "delivery_date": "2025-10-10"
                    },
                    "channels": [
                        "email", "tg"
                        ]
                }
            }
        }
    )
    
):
    try:
        return await TemplateService(db).send_notification(request=request)
    except NotFullBodyRequest:
        raise NotFullBodyRequestHTTPException
    except InvalidTemplateException:
        raise InvalidTemplateHTTPException






