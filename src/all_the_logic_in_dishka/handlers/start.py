from typing import NewType

from aiogram.types import Message
from dishka import AsyncContainer, from_context, provide, Provider, Scope

from all_the_logic_in_dishka.data_structures.user import AddUserDs
from all_the_logic_in_dishka.database.user import AddUserCall


StartHandlerCall = NewType('StartHandlerCall', None)


class StartHandler(Provider):
    scope = Scope.REQUEST
    
    event = from_context(Message)
    
    @provide
    async def handler(
        self,
        event: Message,
        container: AsyncContainer,
    ) -> StartHandlerCall:
        async with container(
            context={
                AddUserDs: AddUserDs(
                    tg_chat_id=event.chat.id,
                    tg_user_id=event.from_user.id,
                ),
            },
        ) as container_action:
            await container_action.get(AddUserCall)
        return StartHandlerCall


async def start_handler(
    event: Message,
    container: AsyncContainer,
) -> None:
    async with container(
        context={
            Message: event,
        },
    ) as next_container:
        await next_container.get(StartHandlerCall)
