from dishka import make_async_container

from src.config import Config
from src.infra.postgres.provider import PostgresProvider
from src.infra.redis.provider import RedisProvider
from src.main.config import config
from src.main.provider import MainProvider

container = make_async_container(
    MainProvider(), PostgresProvider(), RedisProvider(), context={Config: config}
)
