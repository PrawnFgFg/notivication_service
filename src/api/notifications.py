from fastapi import APIRouter, Body




from config import settings
from src.services.templates import TemplateService
from src.api.dependencies import DBDep
from src.schemas.templates import NotificationSendRequestS
from src.exceptions import NotFullBodyRequest, NotFullBodyRequestHTTPException, InvalidTemplateHTTPException, \
    InvalidTemplateException


router = APIRouter(prefix="/notifications", tags=["Уведомления"])



@router.post("/send")
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






"""
# app/api/v1/notifications.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, database, auth, tasks

router = APIRouter(dependencies=[Depends(auth.verify_api_key)])

@router.post("/send", status_code=status.HTTP_202_ACCEPTED)
def send_notification(
    request: schemas.NotificationSendRequest,
    db: Session = Depends(database.get_db)
):
    # 1. Найти шаблон
    template = db.query(models.NotificationTemplate).filter(
        models.NotificationTemplate.key == request.template_key
    ).first()
    
    if not template:
        raise HTTPException(
            stash(log)

    # 4. Отправить задачу в Celery
    tasks.send_notification_task.delay(
        log_itus_code=s=request.user_id,
        context=request.context,
        channels=channels
    )

    # 5. Вернуть ответ
    return {tatus.HTTP_404_NOT_FOUND,
            detail=f"Template '{request.template_key}' not found"
        )

    # 2. Определить каналы
    channels = request.channels or template.default_channels
    if not channels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No channels specified and no default channels in template"
        )

    # 3. Создать запись в логе (статус = queued)
    log = models.NotificationLog(
        user_id=request.user_id,
        template_key=request.template_key,
        context=request.context,
        channels=channels,
        status="queued"
    )
    db.add(log)
    db.commit()
    db.refred=log.id,  # ← лучше передавать ID лога, а не сырые данные
        template_key=request.template_key,
        user_id
        "message": "Notification queued for delivery",
        "log_id": log.id
    }
    
   __________________________________________________________________________________________
   # app/tasks.py
@celery_app.task
def send_notification_task(log_id: int):
    db = SessionLocal()
    try:
        log = db.query(NotificationLog).get(log_id)
        if not log:
            return

        template = db.query(NotificationTemplate).filter_by(key=log.template_key).first()
        if not template:
            log.status = "failed"
            db.commit()
            return

        body = template.body.format(**log.context)
        # ... отправка через SendGrid/Twilio ...
        log.status = "sent"
        db.commit()
    except Exception as e:
        log.status = "failed"
        db.commit()
    finally:
        db.close() 
"""