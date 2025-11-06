from src.connectors.redis_connector import RedisManager
from src.config import settings


redis_manager = RedisManager(
    port=settings.REDIS_PORT,
    host=settings.REDIS_HOST,
)