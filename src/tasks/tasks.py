
from src.tasks.celery_app import celery_instance
from src.tasks.utils import send_message_to_telegram, send_message_to_email, change_logs


@celery_instance.task
def notification_task(
    template_data: dict,
    request_data: dict,
    log_id: int,
):
    if request_data.get("channels"):
        channels: list[str] = request_data.get("channels")
        
    rendered_data = template_data.get("body").format(**request_data.get("body"))
    rendered_data = rendered_data.encode("utf-8")
    
        
    if "channels" not in request_data or "email" in channels:
        recipient_email = request_data.get("body").get("user_email")
        
        resutl_email = send_message_to_email(
            rendered_data=rendered_data, 
            recipient_email=recipient_email
            )
        
    if "tg" in channels:
        tg_id = request_data.get("body").get("telegram_id")
        
        result_tg = send_message_to_telegram(
            rendered_data=rendered_data,
            tg_id=tg_id,
        )
    else:
        result_tg = None
    
    
    change_logs(
        result_email=recipient_email,
        result_tg=result_tg,
        log_id=log_id,
        )
    
        
    
        
    
        
    
    

    
        
        
        
    





    
    


