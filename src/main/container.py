from dishka import make_async_container
from src.main.provider import MainProvider
from src.infra.postgres.provider import PostgresProvider
from src.infra.redis.provider import RedisProvider
from src.config import Config
from src.main.config import config

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    RedisProvider(),
    context={
        Config: config
    }
)