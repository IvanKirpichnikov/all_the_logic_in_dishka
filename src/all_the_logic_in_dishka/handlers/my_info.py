from typing import NewType

from aiogram.types import Message
from dishka import AsyncContainer, from_context, provide, Provider, Scope

from all_the_logic_in_dishka.data_structures.user import UserDs
from all_the_logic_in_dishka.database.user import WithTgUserIdCall


MyInfoHandlerCall = NewType('MyInfoHandlerCall', None)


class MyInfoHandler(Provider):
    scope = Scope.REQUEST
    
    event = from_context(Message)
    
    @provide
    async def handler(
        self,
        event: Message,
        container: AsyncContainer,
    ) -> MyInfoHandlerCall:
        async with container(
            context={
                int: event.from_user.id,
            },
        ) as container_action:
            user: UserDs = await container_action.get(WithTgUserIdCall)
        
        await event.answer(
            f'ID: {user.id}\n'
            f'User telegram id: {user.tg_user_id}\n'
            f'Chat telegram id: {user.tg_chat_id}\n'
            f'Added at: {user.created_at}'
        )
        return MyInfoHandlerCall


async def my_info_handler(
    event: Message,
    container: AsyncContainer,
) -> None:
    async with container(
        context={
            Message: event,
        },
    ) as next_container:
        await next_container.get(MyInfoHandlerCall)
