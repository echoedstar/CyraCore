# © 2026 DragonByte Network | @flexyy

import os
import shutil
import asyncio
import tempfile
from pathlib import Path

from pyrogram import filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.enums import ChatAction

from Cyra import app
from Cyra.helpers import sc

try:
    from pinscrape import Pinterest
except ImportError:
    Pinterest = None


@app.on_message(filters.command(["pinterest", "pin", "pins"]))
async def pinterest_cmd(_, m: Message):
    if Pinterest is None:
        return await m.reply_text(
            "<b>ᴘɪɴꜱᴄʀᴀᴘᴇ ɴᴏᴛ ɪɴꜱᴛᴀʟʟᴇᴅ</b>\n\n"
            "<code>pip install pinscrape</code>\n"
            "ᴘʜɪʀ ʙᴏᴛ ʀᴇꜱᴛᴀʀᴛ ᴋᴀʀᴏ"
        )

    if len(m.command) < 2:
        return await m.reply_text(
            f"<b>{sc('ᴜꜱᴀɢᴇ')}</b>\n<code>/pinterest cute cats</code>"
        )

    query = " ".join(m.command[1:]).strip()
    status = await m.reply_text(
        f"🔍 <b>{sc('ꜱᴇᴀʀᴄʜɪɴɢ')}</b> <code>{query}</code>\n{sc('ᴡᴀɪᴛ...')}"
    )
    temp = None
    try:
        await app.send_chat_action(m.chat.id, ChatAction.UPLOAD_PHOTO)
        temp = tempfile.mkdtemp(prefix="pin_")
        loop = asyncio.get_event_loop()

        def work():
            p = Pinterest(proxies={}, sleep_time=1)
            urls = p.search(query, 12)
            if not urls:
                return []
            p.download(url_list=urls[:12], number_of_workers=6, output_folder=temp)
            files = [
                str(f) for f in Path(temp).rglob("*")
                if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
            ]
            return files[:10]

        files = await loop.run_in_executor(None, work)
        if not files:
            return await status.edit_text(sc("ɴᴏ ɪᴍᴀɢᴇꜱ ꜰᴏᴜɴᴅ"))

        await status.edit_text(f"✅ {len(files)} {sc('ɪᴍᴀɢᴇꜱ')} · {sc('ꜱᴇɴᴅɪɴɢ...')}")
        media = []
        for i, path in enumerate(files):
            cap = f"<b>🔍 {query}</b>\n<i>{sc('ꓚʏ፝֟፝֟ʀᴀ × ᴘɪɴᴛᴇʀᴇꜱᴛ')}</i>" if i == 0 else None
            media.append(InputMediaPhoto(media=path, caption=cap))
        await m.reply_media_group(media)
        await status.delete()
    except Exception as e:
        await status.edit_text(f"❌ <code>{str(e)[:180]}</code>")
    finally:
        if temp and os.path.exists(temp):
            shutil.rmtree(temp, ignore_errors=True)
