
from sqlalchemy.orm import Mapped

from src.database import Base
from src.models.utils import pm_key, str_uniq, str_text


class Templates(Base):
    __tablename__ = "templates"
    
    id: Mapped[pm_key]
    template_key: Mapped[str_uniq]
    body: Mapped[str_text]
    