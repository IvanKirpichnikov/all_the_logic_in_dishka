import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from dishka import make_async_container

from all_the_logic_in_dishka.config import build_config, Config
from all_the_logic_in_dishka.database.connection import ConnectionProvider
from all_the_logic_in_dishka.database.user import UserProvider
from all_the_logic_in_dishka.handlers.my_info import my_info_handler, MyInfoHandler
from all_the_logic_in_dishka.handlers.start import start_handler, StartHandler


async def main(
    config: Config,
) -> None:
    container = make_async_container(
        ConnectionProvider(),
        UserProvider(),
        MyInfoHandler(),
        StartHandler(),
        context={
            Config: config,
        }
    )
    bot = Bot(config.bot.token)
    dispatcher = Dispatcher()
    dispatcher.message(CommandStart())(start_handler)
    dispatcher.message(Command('my'))(my_info_handler)
    dispatcher['container'] = container
    try:
        await dispatcher.start_polling(bot)
    finally:
        await container.close()


def run(
    config_path: Path,
) -> None:
    config = build_config(config_path)
    asyncio.run(main(config))


run(Path('config.toml'))
