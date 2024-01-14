from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.params import Query
from interfaces.services.auth import AuthServiceInterface
from starlette.responses import JSONResponse

router = APIRouter()


@router.post('/login')
async def login(
    auth_service: Annotated[AuthServiceInterface, Depends()],
    phone: Annotated[str, Body(...)],
):
    qr_link = await auth_service.make_qr_code(phone)
    return JSONResponse(
        status_code=201,
        content={'qr_link_url': qr_link},
    )


@router.get('/verify/{token}/{user_id}')
async def verify(
    auth_service: Annotated[AuthServiceInterface, Depends()],
    token: str,
    user_id: int,
):
    result = await auth_service.verify(token, user_id)
    if result:
        return JSONResponse(
            status_code=200,
            content='OK',
        )
    return JSONResponse(
        status_code=403,
        content=None,
    )


@router.get('/check/login')
async def check_login(
    auth_service: Annotated[AuthServiceInterface, Depends()],
    phone: Annotated[str, Query(...)],
):
    status = await auth_service.get_status(phone)
    return JSONResponse(
        status_code=200,
        content={'status': status},
    )
