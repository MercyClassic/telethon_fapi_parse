from typing import Dict, List

from interfaces.repositories.auth import AuthRepositoryInterface
from interfaces.repositories.messages import MessageRepositoryInterface


class MessageService:
    def __init__(
        self,
        auth_repo: AuthRepositoryInterface,
        message_repo: MessageRepositoryInterface,
    ):
        self.auth_repo = auth_repo
        self.message_repo = message_repo

    async def get_messages(
        self,
        phone_number: str,
        username: str,
    ) -> List[Dict[str, str | bool]]:
        messages = await self.message_repo.get_messages(username)
        result = []
        for message in messages:
            result.append(
                {
                    'username': message.username,
                    'is_self': message.from_phone == phone_number,
                    'message_text': message.message_text,
                },
            )
        return result

    async def save_message(
        self,
        message_text: str,
        from_phone: str,
        username: str,
    ) -> str:
        user = await self.auth_repo.get_user(from_phone)
        if not user or user.is_verified is False:
            return 'error'
        await self.message_repo.save_message(
            message_text=message_text,
            from_phone=from_phone,
            username=username,
        )
        return 'ok'
