import asyncio
import smtplib

from src.utils.tg_bot import bot
from src.config import settings






def send_message_to_email(rendered_data: str, recipient_email: str):
    server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.sendmail(settings.SMTP_USER, recipient_email, rendered_data)
    server.quit()









async def send_message_tg(rendered_data, tg_id):
    await bot.send_message(chat_id=tg_id, text=rendered_data)
    await bot.session.close()     
        
        
def send_message_to_telegram(
    rendered_data: str,
    tg_id: str,
):
    asyncio.run(send_message_tg(rendered_data, tg_id))
