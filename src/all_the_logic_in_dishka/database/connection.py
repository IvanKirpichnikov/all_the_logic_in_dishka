from typing import AsyncIterable

from aiosqlite import connect, Connection
from dishka import from_context, provide, Provider, Scope

from all_the_logic_in_dishka.config import Config


class ConnectionProvider(Provider):
    scope = Scope.APP
    
    config = from_context(Config)
    
    @provide
    async def connection(
        self,
        config: Config,
    ) -> AsyncIterable[Connection]:
        async with connect(config.database.url) as connection:
            yield connection
