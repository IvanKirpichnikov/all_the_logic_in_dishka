from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddUserDs:
    tg_user_id: int
    tg_chat_id: int


@dataclass
class UserDs:
    id: int
    tg_user_id: int
    tg_chat_id: int
    created_at: datetime
