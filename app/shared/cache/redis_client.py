from redis import asyncio as redis

from app.config.settings import settings


redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


async def get_redis():

    return redis_client