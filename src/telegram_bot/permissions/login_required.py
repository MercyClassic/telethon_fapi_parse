from typing import Callable

from api_client import APIClient
from cache import Cache
from telethon import TelegramClient, events


def login_required(func: Callable) -> Callable:
    async def decorator(
        event: events.NewMessage.Event,
        bot: TelegramClient,
        cache: Cache,
        api_client: APIClient,
    ):
        user_id = event.peer_id.user_id
        user_info = cache.get(user_id)
        if not user_info:
            await bot.send_message(
                entity=user_id,
                message='Для начала пройдите аутентификацию',
            )
            return
        if user_info.get('is_authenticated') is False:
            await bot.send_message(
                entity=user_id,
                message='Для вызова этой команды следует пройти авторизацию',
            )

        result = await func(event, bot, cache, api_client)
        return result

    return decorator
