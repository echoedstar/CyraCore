# © 2026 DragonByte Network | @flexyy

import random
from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import IMG, SUPPORT_GROUP, UPDATES_CHANNEL, SUPPORT_CHAT_LINK
from Cyra import app, START_TIME
from Cyra.database import get_stats
from Cyra.helpers import sc

boot = datetime.now()


@app.on_message(filters.command("ping"))
async def ping_cmd(_, m: Message):
    start = datetime.now()
    msg = await m.reply_text(sc("ᴘɪɴɢɪɴɢ..."))
    ms = (datetime.now() - start).microseconds / 1000
    up = datetime.now() - boot
    h, r = divmod(int(up.total_seconds()), 3600)
    mi, s = divmod(r, 60)
    await msg.delete()
    await m.reply_photo(
        photo=random.choice(IMG),
        caption=(
            f"<b>{sc('ᴘᴏɴɢ')}</b> <code>{ms:.0f}</code> ᴍꜱ\n"
            f"<b>{sc('ᴜᴘᴛɪᴍᴇ')}</b> <code>{h}ʜ:{mi}ᴍ:{s}ꜱ</code>\n\n"
            f"<i>{sc('ꓚʏ፝֟፝֟ʀᴀ ɪꜱ ᴀʟɪᴠᴇ')}</i>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(sc("ꜱᴜᴘᴘᴏʀᴛ"), url=SUPPORT_CHAT_LINK),
                InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url=f"https://t.me/{UPDATES_CHANNEL}"),
            ]
        ]),
    )


@app.on_message(filters.command("stats"))
async def stats_cmd(_, m: Message):
    users, chats = await get_stats()
    await m.reply_text(
        f"<b>{sc('ꓚʏ፝֟፝֟ʀᴀ ꜱᴛᴀᴛꜱ')}</b>\n\n"
        f"• {sc('ᴜꜱᴇʀꜱ')} : <code>{users}</code>\n"
        f"• {sc('ɢʀᴏᴜᴘꜱ')} : <code>{chats}</code>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("ᴀᴅᴅ ᴍᴇ"), url=f"https://t.me/{app.username}?startgroup=true")]
        ]),
    )
