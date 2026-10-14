import json
import logging
import redis

logger = logging.getLogger(__name__)
client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)

def get_cache(key: str):
    try:
        value = client.get(key)
        return json.loads(value) if value is not None else None
    except (redis.RedisError, ValueError) as exc:
        logger.warning("Redis cache read failed: %s", exc)
        return None

def set_cache(key: str, value, ttl: int = 3600):
    try:
        client.set(key, json.dumps(value), ex=ttl)
    except (redis.RedisError, TypeError, ValueError) as exc:
        logger.warning("Redis cache write failed: %s", exc)
