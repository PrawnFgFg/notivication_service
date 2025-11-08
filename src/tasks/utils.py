import asyncio
import smtplib

from src.utils.tg_bot import bot
from src.config import settings
from src.utils.db_manager import DBManager
from src.schemas.notification_logs import NotificationLogUpdtStatusS
from src.database import assync_session_maker





def send_message_to_email(rendered_data: str, recipient_email: str):
    server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.sendmail(settings.SMTP_USER, recipient_email, rendered_data)
    server.quit()
    return True



async def send_message_tg(rendered_data, tg_id):
    await bot.send_message(chat_id=tg_id, text=rendered_data)
    await bot.session.close()     
        
        
def send_message_to_telegram(
    rendered_data: str,
    tg_id: str,
):
    asyncio.run(send_message_tg(rendered_data, tg_id))
    return True




async def change_logs_async(result_email: bool, result_tg: bool, log_id: int):
    if result_email or result_tg:
        status_log = "sent"
    else:
        status_log = "failed"
    
    async with DBManager() as db:
        await db.notification_logs.edit(
            schema_to_update=NotificationLogUpdtStatusS(status=status_log),
            exclude_unset=True,
            id=log_id
        )
        a = await db.notification_logs.get_one_by_filter(id=log_id)
        await db.commit()
   
    
def change_logs(result_email: bool, result_tg: bool, log_id: int):
    asyncio.run(change_logs_async(
        result_email, result_tg, log_id,
    ))
        
        
        