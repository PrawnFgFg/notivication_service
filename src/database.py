from sqlalchemy import NullPool, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from src.config import settings
 



engine = create_async_engine(url=settings.DB_URL)
engine_null_pool = create_async_engine(url=settings.DB_URL, poolclass=NullPool)

assync_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)





class Base(DeclarativeBase):
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())