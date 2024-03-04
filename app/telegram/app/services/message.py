from typing import Optional, NoReturn

import asyncio

from telegram.app import schemas
from telegram.app.config import bot_init, settings


async def message_send(message: schemas.PlainMessageSend) -> Optional[NoReturn]:
    async with await bot_init() as bot:
        await bot.send_message(settings.TG_FILES_CHAT_ID, message.text)


async def photo_send(message: schemas.PlainMessageSend) -> Optional[NoReturn]:
    async with await bot_init() as bot:
        await bot.send_file(settings.TG_FILES_CHAT_ID, message.image_url, caption=message.text)


async def message_send_multiple(messages: list[schemas.PlainMessageSend]) -> Optional[NoReturn]:
    async with bot_init() as bot:
        await asyncio.gather(*[bot.send_message(msg.chat_id, msg.text) for msg in messages])

