# © 2026 DragonByte Network | @flexyy

import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import OWNER_ID
from Cyra import app
from Cyra.database import usersdb, chatsdb
from Cyra.helpers import sc


@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_cmd(_, m: Message):
    reply = m.reply_to_message
    text = m.text.split(None, 1)[1] if len(m.command) > 1 else None
    if not reply and not text:
        return await m.reply_text(sc("ʀᴇᴘʟʏ ᴏʀ ɢɪᴠᴇ ᴛᴇxᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ"))

    status = await m.reply_text(sc("ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ..."))
    ok = fail = 0

    targets = []
    async for u in usersdb.find({}, {"user_id": 1}):
        targets.append(u["user_id"])
    async for c in chatsdb.find({}, {"chat_id": 1}):
        targets.append(c["chat_id"])

    for cid in targets:
        try:
            if reply:
                await reply.copy(cid)
            else:
                await app.send_message(cid, text)
            ok += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if reply:
                    await reply.copy(cid)
                else:
                    await app.send_message(cid, text)
                ok += 1
            except Exception:
                fail += 1
        except Exception:
            fail += 1

    await status.edit_text(
        f"<b>{sc('ᴅᴏɴᴇ')}</b>\n"
        f"✅ {ok}\n❌ {fail}"
    )
