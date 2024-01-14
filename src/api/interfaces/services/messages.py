from abc import ABC, abstractmethod


class MessageServiceInterface(ABC):
    @abstractmethod
    async def get_messages(
        self,
        phone_number: str,
        username: str,
    ):
        pass

    @abstractmethod
    async def save_message(
        self,
        message_text: str,
        from_phone: str,
        username: str,
    ):
        pass
