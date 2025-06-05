from redis.asyncio import Redis

redis: Redis = None


async def connect_redis():
    global redis
    redis = Redis(host="redis", port=6379, decode_responses=True)


async def disconnect_redis():
    global redis
    if redis:
        await redis.close()
