import os
from functools import partial

from db.database import create_async_session_maker, get_async_session
from di.dependencies.auth import get_auth_repository, get_auth_service
from di.dependencies.messages import get_message_repository, get_message_service
from di.dependencies.session_stub import get_session_stub
from fastapi import FastAPI
from interfaces.repositories.auth import AuthRepositoryInterface
from interfaces.repositories.messages import MessageRepositoryInterface
from interfaces.services.auth import AuthServiceInterface
from interfaces.services.messages import MessageServiceInterface


def init_dependencies(app: FastAPI):
    async_session_maker = create_async_session_maker('sqlite+aiosqlite:///sqlite.db')

    app.dependency_overrides[get_session_stub] = partial(
        get_async_session,
        async_session_maker,
    )
    app.dependency_overrides[AuthRepositoryInterface] = get_auth_repository
    app.dependency_overrides[MessageRepositoryInterface] = get_message_repository
    app.dependency_overrides[AuthServiceInterface] = partial(
        get_auth_service,
        os.environ['api_url'],
    )
    app.dependency_overrides[MessageServiceInterface] = get_message_service
