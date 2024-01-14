from typing import Sequence

from db.models import Message
from interfaces.repositories.messages import MessageRepositoryInterface
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository(MessageRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_messages(
        self,
        username: str,
    ) -> Sequence[Message]:
        query = select(Message).where(Message.username == username).limit(50)
        return (await self._session.execute(query)).scalars().all()

    async def save_message(
        self,
        message_text: str,
        from_phone: str,
        username: str,
    ) -> None:
        stmt = insert(Message).values(
            message_text=message_text,
            from_phone=from_phone,
            username=username,
        )
        await self._session.execute(stmt)
        await self._session.commit()
