from typing import Annotated

from db.repositories.auth import AuthRepository
from di.dependencies.session_stub import get_session_stub
from fastapi import Depends
from interfaces.repositories.auth import AuthRepositoryInterface
from services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession


def get_auth_repository(
    session: Annotated[AsyncSession, Depends(get_session_stub)],
) -> AuthRepository:
    return AuthRepository(session)


def get_auth_service(
    api_url: str,
    auth_repo: Annotated[AuthRepositoryInterface, Depends()],
) -> AuthService:
    return AuthService(api_url=api_url, auth_repo=auth_repo)
