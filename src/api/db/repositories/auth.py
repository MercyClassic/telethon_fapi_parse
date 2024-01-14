from db.models import User
from db.models.user import Token
from interfaces.repositories.auth import AuthRepositoryInterface
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class AuthRepository(AuthRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user(self, phone_number: str) -> User:
        query = select(User).where(User.phone_number == phone_number)
        return (await self._session.execute(query)).scalar()

    async def save_user(self, phone_number: str) -> User:
        stmt = insert(User).values(phone_number=phone_number, is_verified=False).returning(User)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar()

    async def save_token(self, token: str, user_id: int) -> None:
        stmt = insert(Token).values(token=token, user_id=user_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_token(self, token: str) -> Token:
        query = select(Token).where(Token.token == token).options(joinedload(Token.user))
        return (await self._session.execute(query)).scalar()

    async def verify_user(self, user_id: int) -> None:
        stmt = update(User).where(User.id == user_id).values(is_verified=True)
        await self._session.execute(stmt)
        await self._session.commit()
