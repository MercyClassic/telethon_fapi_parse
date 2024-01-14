from functools import partial
from typing import Callable

from api_client import APIClient
from cache import Cache
from telethon import TelegramClient


class Router:
    def __init__(self):
        self._handlers = {}

    def register_handlers(
        self,
        bot: TelegramClient,
        cache: Cache,
        api_client: APIClient,
    ):
        for func, event in self._handlers.items():
            handler = partial(
                func,
                bot=bot,
                cache=cache,
                api_client=api_client,
            )
            bot.on(event)(handler)

    def handle(self, event):
        def decorator(func: Callable):
            self._handlers.update({func: event})
            return func

        return decorator
