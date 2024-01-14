from api_client import APIClient
from cache import Cache
from permissions import login_required
from routers.router import Router
from telethon import TelegramClient, events

router = Router()


@router.handle(events.NewMessage(pattern='/send_message'))
@login_required
async def send_message(
    event: events.NewMessage.Event,
    bot: TelegramClient,
    cache: Cache,
    api_client: APIClient,
):
    try:
        username, message = event.text.split(maxsplit=2)[1:]
    except ValueError:
        await bot.send_message(
            entity=event.peer_id,
            message='Не обнаружен @username или сообщение, повторите попытку',
        )
        return

    await bot.send_message(
        entity=event.peer_id,
        message='Отправляем сообщение...',
    )

    try:
        await bot.send_message(
            username,
            message=message,
        )
    except ValueError:
        await bot.send_message(
            entity=event.peer_id,
            message='Пользователя с таким @username не существует!',
        )
        return

    phone_number = cache.get(event.peer_id.user_id).get('phone_number')
    status = await api_client.send_message(phone_number, username, message)
    if status == 201:
        await bot.send_message(
            entity=event.peer_id,
            message='Сообщение отправлено!',
        )
    else:
        await bot.send_message(
            entity=event.peer_id,
            message='Oops, something went wrong!',
        )


def build_message(messages: dict) -> str:
    message = ''
    for mes in messages:
        message += (
            f"От меня: {mes['is_self']}"
            f"\nusername: {mes['username']}"
            f"\nСообщение: {mes['message_text']}\n\n"
        )
    return message


@router.handle(events.NewMessage(pattern='/get_messages'))
@login_required
async def get_messages(
    event: events.NewMessage.Event,
    bot: TelegramClient,
    cache: Cache,
    api_client: APIClient,
):
    await bot.send_message(
        entity=event.peer_id,
        message='Получаем сообщения...',
    )

    try:
        username = event.text.split(maxsplit=1)[1]
    except ValueError:
        await bot.send_message(
            entity=event.peer_id,
            message='Не обнаружен @username, повторите попытку',
        )
        return

    phone_number = cache.get(event.peer_id.user_id).get('phone_number')
    messages = await api_client.get_messages(phone_number, username)
    await bot.send_message(
        entity=event.peer_id,
        message=build_message(messages),
    )
