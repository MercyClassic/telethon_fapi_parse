import uuid

from interfaces.repositories.auth import AuthRepositoryInterface


class AuthService:
    def __init__(self, api_url: str, auth_repo: AuthRepositoryInterface):
        self.api_url = api_url
        self.repo = auth_repo

    async def make_qr_code(self, phone_number: str) -> str:
        user = await self.repo.get_user(phone_number)
        if not user:
            user = await self.repo.save_user(phone_number)
        token = str(uuid.uuid4())
        await self.repo.save_token(token, user.id)
        qr_link = f'{self.api_url}/verify/{token}/{user.id}'
        return qr_link

    async def verify(self, token: str, user_id: int):
        token = await self.repo.get_token(token)
        if not token or token.user_id != user_id:
            return False
        await self.repo.verify_user(user_id)
        return True

    async def get_status(self, phone_number: str) -> str:
        user = await self.repo.get_user(phone_number)
        if not user:
            return 'error'
        if user.is_verified:
            return 'logined'
        if not user.is_verified:
            return 'waiting_qr_login'
