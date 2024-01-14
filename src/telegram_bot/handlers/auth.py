import io
import re

import qrcode
from api_client import APIClient
from cache import Cache
from factory.api_client import get_api_client
from permissions import phone_number_recognized
from routers.router import Router
from telethon import TelegramClient, events

router = Router()


async def is_user_authenticated(
    cache: Cache,
    api_client: APIClient,
    user_id: int,
    phone_number: str,
):
    user_info = cache.get(user_id)
    if user_info:
        if user_info.get('is_authenticated'):
            return True
    status = await api_client.get_login_status(phone_number)
    cache.set(
        {
            user_id: {
                'phone_number': phone_number,
                'is_authenticated': True if status == 'logined' else False,
            },
        },
    )
    if status == 'logined':
        return True
    return False


def get_qr_code_image(qr_link: str):
    qr_code = qrcode.make(qr_link)
    img = io.BytesIO()
    img.name = 'qr_code.jpg'
    qr_code.save(img, 'jpeg')
    img.seek(0)
    return img


@router.handle(events.NewMessage(pattern='/login'))
@phone_number_recognized
async def login(
    event: events.NewMessage.Event,
    bot: TelegramClient,
    cache: Cache,
    api_client: APIClient,
):
    phone_number = event.text.split(maxsplit=1)[1]
    normalized_phone_numer = re.sub(r'[()+ -]*', '', phone_number)
    user_id = event.peer_id.user_id
    if await is_user_authenticated(cache, api_client, user_id, phone_number):
        await bot.send_message(
            entity=event.peer_id.user_id,
            message='Вы успешно аутентифицировались!',
        )
        return
    qr_link = await api_client.get_qr_link(normalized_phone_numer)
    img = get_qr_code_image(qr_link)
    await bot.send_message(
        entity=event.peer_id,
        message='Чтобы залогиниться, пройдите по ссылке из QR кода',
        file=img,
    )


@router.handle(events.NewMessage(pattern='/check_login'))
@phone_number_recognized
async def check_login(
    event: events.NewMessage.Event,
    bot: TelegramClient,
    *args,
    **kwargs,
):
    phone_number = event.text.split(maxsplit=1)[1]
    normalized_phone_numer = re.sub(r'[()+ -]*', '', phone_number)
    api_client = get_api_client()
    status = await api_client.get_login_status(normalized_phone_numer)
    await bot.send_message(
        entity=event.peer_id,
        message=status,
    )
