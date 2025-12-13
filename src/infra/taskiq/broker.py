from __future__ import annotations

from loguru import logger
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from src.config import RedisConfig
from src.main.config import config


def _build_dsn(redis_config: RedisConfig) -> str:
    password = f":{redis_config.password}@" if redis_config.password else ""
    return f"redis://{password}{redis_config.host}:{redis_config.port}/{redis_config.db}"


def create_broker(redis_config: RedisConfig | None = None) -> ListQueueBroker:
    cfg = redis_config or RedisConfig()
    if redis_config is None:
        logger.warning("Redis config is missing. Using default Redis settings for TaskIQ broker.")
    dsn = _build_dsn(cfg)
    broker = ListQueueBroker(dsn)
    broker.with_result_backend(RedisAsyncResultBackend(dsn))
    return broker


broker = create_broker(config.redis)
