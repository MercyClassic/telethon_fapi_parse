from abc import ABC, abstractmethod


class AuthServiceInterface(ABC):
    @abstractmethod
    async def make_qr_code(self, phone_number: str) -> str:
        pass

    @abstractmethod
    async def verify(self, token: str, user_id: int) -> str:
        pass

    @abstractmethod
    async def get_status(self, phone_number: str):
        pass
