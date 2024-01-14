from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from interfaces.services.messages import MessageServiceInterface
from pydantic import BaseModel
from starlette.responses import JSONResponse

router = APIRouter()


class Message(BaseModel):
    message_text: str = Body(...)
    from_phone: str = Body(...)
    username: str = Body(...)


@router.post('/messages')
async def save_message(
    message_service: Annotated[MessageServiceInterface, Depends()],
    message_data: Message,
):
    result = await message_service.save_message(
        message_text=message_data.message_text,
        from_phone=message_data.from_phone,
        username=message_data.username,
    )
    return JSONResponse(
        status_code=201 if result == 'ok' else 403,
        content=result,
    )


@router.get('/messages')
async def get_messages(
    message_service: Annotated[MessageServiceInterface, Depends()],
    phone: Annotated[str, Query(...)],
    uname: Annotated[str, Query(...)],
):
    data = await message_service.get_messages(
        phone_number=phone,
        username=uname,
    )
    return JSONResponse(
        status_code=200,
        content={'messages': data},
    )
