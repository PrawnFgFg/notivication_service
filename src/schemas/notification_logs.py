from datetime import date
from pydantic import BaseModel




class NotificationLogS(BaseModel):
    
    user_id: int
    template_key: str
    body: dict
    channels: list
    status: str
    sent_at: date
    
    
class NotificationLogUpdtStatusS(BaseModel):
    status: str