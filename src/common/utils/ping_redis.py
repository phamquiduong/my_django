import logging

import redis

logger = logging.getLogger()


def check_redis(redis_url: str) -> bool:
    try:
        redis.StrictRedis.from_url(redis_url, socket_connect_timeout=2).ping()
        return True
    except Exception as exc:
        logger.warning("Redis unavailable: %s", exc)
        return False
