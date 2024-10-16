from datetime import datetime
from typing import Final, NewType

from aiosqlite import Connection
from dishka import from_context, provide, Provider, Scope

from all_the_logic_in_dishka.data_structures.user import AddUserDs, UserDs


AddUserCall = NewType('AddUserCall', None)
WithTgUserIdCall = NewType('CreateUserAction', UserDs)

ADD_QUERY: Final = '''
    INSERT INTO users(
        tg_user_id,
        tg_chat_id,
        created_at
    )
    VALUES(?, ?, ?);
'''

WITH_TG_USER_ID_QUERY: Final = '''
    SELECT
        id,
        tg_user_id,
        tg_chat_id,
        created_at
    FROM users
    WHERE tg_user_id = ?;
'''


class UserProvider(Provider):
    scope = Scope.ACTION
    
    data_structures = (
        from_context(AddUserDs)
        + from_context(int)
    )
    
    @provide
    async def add(
        self,
        data: AddUserDs,
        connection: Connection,
    ) -> AddUserCall:
        async with connection.execute(
            ADD_QUERY,
            (data.tg_user_id, data.tg_chat_id, datetime.now()),
        ):
            return AddUserCall
    
    @provide
    async def with_tg_user_id(
        self,
        tg_user_id: int,
        connection: Connection,
    ) -> WithTgUserIdCall:
        async with connection.execute(
            WITH_TG_USER_ID_QUERY,
            (tg_user_id,),
        ) as cursor:
            data = await cursor.fetchone()
        return WithTgUserIdCall(
            UserDs(
                id=data[0],
                tg_user_id=data[1],
                tg_chat_id=data[2],
                created_at=data[3],
            ),
        )
