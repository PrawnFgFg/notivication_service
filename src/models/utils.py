import enum
from typing import Annotated
from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column




class EnumRole(enum.Enum):
    
    user = "user"
    admin = "admin"
    
pm_key = Annotated[int, mapped_column(primary_key=True)]
length_str_200 = Annotated[str, mapped_column(String(200))]
length_str_200_uniq = Annotated[str, mapped_column(String(200), unique=True)] 
str_uniq = Annotated[str, mapped_column(unique=True)]
length_str_20 = Annotated[str, mapped_column(String(20))]
enum_role = Annotated[EnumRole, mapped_column(default=EnumRole.user, server_default="user")]
str_text = Annotated[str, mapped_column(Text())]

