from app.core.redis import redis_client

CACHE_TTL    = 3600
CACHE_PREFIX = "url:"

async def get_cached_url(short_code: str) -> str | None:
    return await redis_client.get(f"{CACHE_PREFIX}{short_code}")

async def set_cached_url(short_code: str, original_url: str) -> None:
    await redis_client.setex(f"{CACHE_PREFIX}{short_code}", CACHE_TTL, original_url)

async def delete_cached_url(short_code: str) -> None:
    await redis_client.delete(f"{CACHE_PREFIX}{short_code}")