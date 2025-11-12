from dishka import Provider
from dishka import Scope
from dishka import from_context
from dishka import provide
from dishka import provide_all
from fastapi import Request

from src.config import Config
from src.config import ApiConfig
from src.config import DatabaseConfig
from src.config import RedisConfig

from src.usecase.users.create import CreateUserUsecase
from src.usecase.cards.update import UpdateCardUsecase

class MainProvider(Provider):
    scope = Scope.REQUEST

    _provide_config = from_context(provides=Config, scope=Scope.APP) 

    @provide(scope=Scope.APP)
    async def _get_api_config(self, config: Config) -> ApiConfig:
        return config.api
    
    @provide(scope=Scope.APP)
    async def _get_database_config(self, config: Config) -> DatabaseConfig:
        return config.database
    
    @provide(scope=Scope.APP)
    async def _get_redis_config(self, config: Config) -> RedisConfig | None:
        return config.redis

    _request = from_context(provides=Request, scope=Scope.REQUEST)

    _get_usecases = provide_all(
        CreateUserUsecase,
        UpdateCardUsecase,
    )

