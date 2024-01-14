from parser import Product
from typing import List

from factory.parser import get_parser
from routers.router import Router
from telethon import TelegramClient, events

router = Router()


def build_message(products: List[Product]) -> str:
    message = ''
    for product in products:
        message += f'Название товара:\n "{product.title}"\nСсылка: {product.link}\n\n'
    return message


@router.handle(events.NewMessage(pattern='wild: '))
async def parse(
    event: events.NewMessage.Event,
    bot: TelegramClient,
    *args,
    **kwargs,
):
    parser = get_parser()
    product_name = event.text.split(': ', maxsplit=1)[1]

    await bot.send_message(
        entity=event.peer_id,
        message='Запрос принят, пожалуйста подождите!',
    )

    data = await parser.parse(product_name)
    message = build_message(data)

    await bot.send_message(
        entity=event.peer_id,
        message=message,
    )
