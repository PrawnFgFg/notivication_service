from sqlalchemy.orm import Mapped, mapped_column



from src.database import Base
from src.models.utils import length_str_200, length_str_20, enum_role, length_str_200_uniq, pm_key



class User(Base):
    __tablename__ = "users"
    
    id: Mapped[pm_key]
    email: Mapped[length_str_200_uniq]
    hashed_password: Mapped[length_str_200]
    nickname: Mapped[length_str_20]
    role: Mapped[enum_role]
    
    

    
    