import io
from typing import Optional, NoReturn

import asyncio
from fastapi import UploadFile
from telethon.utils import pack_bot_file_id

from telegram.app import schemas
from telegram.app.config import bot_init, settings


async def tg_document_create(document: UploadFile) -> dict[str, Optional[str]]:
    doc_bytes = io.BytesIO(document.file.read())
    doc_bytes.name = document.filename

    async with await bot_init() as bot:
        msg = await bot.send_file(settings.TG_FILES_CHAT_ID, doc_bytes)

    tg_doc_id = pack_bot_file_id(msg.media)
    return {'document_id': tg_doc_id}


async def document_send(message: schemas.DocumentSend) -> Optional[NoReturn]:
    async with await bot_init() as bot:
        await bot.send_file(
                entity=settings.TG_FILES_CHAT_ID,
                file=message.document_id,
                caption=message.caption,
        )


async def document_send_multiple(messages: list[schemas.DocumentSend]) -> Optional[NoReturn]:
    async with await bot_init() as bot:
        await asyncio.gather(*[
                bot.send_file(
                    entity=settings.TG_FILES_CHAT_ID,
                    file=msg.document_id,
                    caption=msg.caption,
                ) for msg in messages
            ]
        )
