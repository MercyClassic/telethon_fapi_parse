from typing import Annotated

from db.repositories.messages import MessageRepository
from di.dependencies.session_stub import get_session_stub
from fastapi import Depends
from interfaces.repositories.auth import AuthRepositoryInterface
from interfaces.repositories.messages import MessageRepositoryInterface
from services.messages import MessageService
from sqlalchemy.ext.asyncio import AsyncSession


def get_message_repository(
    session: Annotated[AsyncSession, Depends(get_session_stub)],
) -> MessageRepository:
    return MessageRepository(session)


def get_message_service(
    auth_repo: Annotated[AuthRepositoryInterface, Depends()],
    message_repo: Annotated[MessageRepositoryInterface, Depends()],
) -> MessageService:
    return MessageService(
        auth_repo=auth_repo,
        message_repo=message_repo,
    )
