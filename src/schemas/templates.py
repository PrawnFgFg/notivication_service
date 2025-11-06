from pydantic import BaseModel
from typing import List

from src.config import settings

class NotificationSendRequestS(BaseModel):
    
    template_key: str
    user_id: int
    body: dict = {
        "username": "string",
        "order_id": 0,
        "user_email": "example@gmail.com",
        "telegram_id": 0,
        "delivery_date": "2025-10-10"
    }
    channels: List[str] = ["email"]
    
    
class NotificationSendS(BaseModel):
    template_key: str
    body: str