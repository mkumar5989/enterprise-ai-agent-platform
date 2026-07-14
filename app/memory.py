import json
from redis.asyncio import Redis
from app.core.config import settings

redis = Redis.from_url(settings.redis_url, decode_responses=True)

async def store_memory(session_id: str, payload: dict):
    await redis.set(
        f"agent-memory:{session_id}",
        json.dumps(payload),
        ex=settings.memory_ttl_seconds,
    )

async def get_memory(session_id: str) -> dict:
    raw = await redis.get(f"agent-memory:{session_id}")
    return json.loads(raw) if raw else {}
