import re
from typing import Callable

from telethon import TelegramClient, events


async def phone_number_dont_recognized(
    peer_id: int,
    bot: TelegramClient,
) -> None:
    await bot.send_message(
        entity=peer_id,
        message='Номер телефона не распознан, попробуйте ещё раз',
    )


def phone_number_recognized(func: Callable) -> Callable:
    async def decorator(
        event: events.NewMessage.Event,
        bot: TelegramClient,
        *args,
        **kwargs,
    ):
        try:
            phone_number = event.text.split(maxsplit=1)[1]
        except IndexError:
            await phone_number_dont_recognized(event.peer_id, bot)
            return

        if not re.fullmatch(
            r'\+?[7, 8]-?\s*-?\(?\d{3}\)?-?\s*-?\d{3}-?\s*-?\d{2}-?\s*-?\d{2}',
            phone_number,
            flags=re.ASCII,
        ):
            await phone_number_dont_recognized(event.peer_id, bot)
            return

        result = await func(event, bot, *args, **kwargs)
        return result

    return decorator
