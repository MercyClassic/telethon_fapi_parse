from abc import ABC, abstractmethod


class AuthRepositoryInterface(ABC):
    @abstractmethod
    async def get_user(self, phone_number: str):
        pass

    @abstractmethod
    async def save_user(self, phone_number: str):
        pass

    @abstractmethod
    async def save_token(self, token: str, user_id: int):
        pass

    @abstractmethod
    async def get_token(self, token: str):
        pass

    @abstractmethod
    async def verify_user(self, user_id: int):
        pass
