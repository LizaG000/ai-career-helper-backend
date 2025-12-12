from dishka import Provider, Scope, from_context, provide, provide_all
from fastapi import Request

from src.config import ApiConfig, Config, DatabaseConfig, RedisConfig
from src.usecase.cards.create import CreateCardsUsecase
from src.usecase.cards.delete import DeleteCardUsecase
from src.usecase.cards.generate import GenerateCardsUsecase
from src.usecase.cards.get_all import GetAllCardsUsecase
from src.usecase.cards.update import UpdateCardUsecase
from src.usecase.user_careers.create import CreateUserCareerUsecase
from src.usecase.users.create import CreateUserUsecase


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
        DeleteCardUsecase,
        UpdateCardUsecase,
        CreateUserCareerUsecase,
        GetAllCardsUsecase,
        CreateCardsUsecase,
        GenerateCardsUsecase,
    )
