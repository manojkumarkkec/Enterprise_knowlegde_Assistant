import json


class CacheService:


    def __init__(
        self,
        redis,
    ):
        self.redis = redis



    async def get(
        self,
        key:str,
    ):

        value = await self.redis.get(
            key
        )


        if value:

            return json.loads(value)


        return None



    async def set(
        self,
        key:str,
        value,
        expire=3600,
    ):

        await self.redis.set(
            key,
            json.dumps(value),
            ex=expire,
        )