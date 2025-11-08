from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON



from src.database import Base
from src.models.utils import pm_key, str_uniq


class NotificationLogs(Base):
    __tablename__ = "notificationlogs"
    
    id: Mapped[pm_key]
    user_id: Mapped[int]
    template_key: Mapped[str]
    body: Mapped[dict] = mapped_column(JSON)
    channels: Mapped[list[str]] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(default="queued", server_default="queued")
    sent_at: Mapped[date]
    