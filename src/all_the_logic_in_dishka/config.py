import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BotConfig:
    token: str

@dataclass
class DatabaseConfig:
    url: str


@dataclass
class Config:
    bot: BotConfig
    database: DatabaseConfig


def build_config(path: Path) -> Config:
    with path.open('rb') as file:
        data = tomllib.load(file)
    
    return Config(
        bot=BotConfig(
            token=data['bot']['token'],
        ),
        database=DatabaseConfig(
            url=data['database']['url'],
        ),
    )
