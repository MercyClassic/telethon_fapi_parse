import os

from factory.api_client import get_api_client
from factory.cache import get_cache
from handlers import auth_router, messages_router, parse_router
from telethon import TelegramClient


def main():
    bot_token = os.environ['bot_token']
    api_id = int(os.environ['api_id'])
    api_hash = os.environ['api_hash']
    bot = TelegramClient('bot', api_id, api_hash)
    bot.start(bot_token=bot_token)

    cache = get_cache()
    api_client = get_api_client()

    auth_router.register_handlers(bot, cache, api_client)
    parse_router.register_handlers(bot, cache, api_client)
    messages_router.register_handlers(bot, cache, api_client)

    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
