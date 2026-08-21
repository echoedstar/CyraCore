# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ChatType

from config import IMG, OWNER_ID, SUPPORT_GROUP, UPDATES_CHANNEL, SUPPORT_CHAT_LINK, LOGGER_GROUP_ID
from Cyra import app
from Cyra.database import add_user, add_chat
from Cyra.helpers import sc


def start_btns():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("ᴀᴅᴅ ᴍᴇ"), url=f"https://t.me/{app.username}?startgroup=true")],
        [
            InlineKeyboardButton(sc("ꜱᴜᴘᴘᴏʀᴛ"), url=SUPPORT_CHAT_LINK),
            InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url=f"https://t.me/{UPDATES_CHANNEL}"),
        ],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ"), callback_data="help")],
    ])


START_TEXT = (
    f"<b>{sc('ʜᴇʏ ɪ ᴀᴍ')} ꓚʏ፝֟፝֟ʀᴀ</b>\n\n"
    f"<i>{sc('ᴀ ᴄᴜᴛᴇ ʜᴇʟᴘᴇʀ ʙᴏᴛ ꜰᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ & ᴘᴍ')}</i>\n\n"
    f"• {sc('ᴘɪɴᴛᴇʀᴇꜱᴛ ᴘʜᴏᴛᴏꜱ')}\n"
    f"• {sc('ᴍᴏᴠɪᴇ / ꜱᴇʀɪᴇꜱ ꜱᴇᴀʀᴄʜ')}\n"
    f"• {sc('ɢʀᴏᴜᴘ ᴛᴏᴏʟꜱ')}\n\n"
    f"<b>{sc('ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴅʀᴀɢᴏɴʙʏᴛᴇ ɴᴇᴛᴡᴏʀᴋ')}</b>"
)

HELP_TEXT = (
    f"<b>{sc('ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ')}</b>\n\n"
    f"<b>{sc('ᴜꜱᴇʀꜱ')}</b>\n"
    f"/start — {sc('ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ')}\n"
    f"/help — {sc('ʜᴇʟᴘ ᴍᴇɴᴜ')}\n"
    f"/ping — {sc('ᴄʜᴇᴄᴋ ʟᴀᴛᴇɴᴄʏ')}\n"
    f"/stats — {sc('ʙᴏᴛ ꜱᴛᴀᴛꜱ')}\n"
    f"/id — {sc('ʏᴏᴜʀ ɪᴅ')}\n"
    f"/pinterest <q> — {sc('10 ᴘɪɴᴛᴇʀᴇꜱᴛ ᴘʜᴏᴛᴏꜱ')}\n"
    f"/pin <q> — {sc('ꜱᴀᴍᴇ ᴀꜱ ᴘɪɴᴛᴇʀᴇꜱᴛ')}\n"
    f"/tmdb <q> — {sc('ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ / ꜱᴇʀɪᴇꜱ')}\n"
    f"/poster — {sc('ᴘᴏꜱᴛᴇʀꜰᴏʀɢᴇ ꜱᴛᴜᴅɪᴏ ʜᴇʟᴘ')}\n"
    f"/setchannel <name> — {sc('ᴘᴏꜱᴛᴇʀ ᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇ')}\n\n"
    f"<b>{sc('ɢʀᴏᴜᴘ')}</b>\n"
    f"/id — {sc('ᴄʜᴀᴛ & ᴜꜱᴇʀ ɪᴅ')}\n\n"
    f"<b>{sc('ᴏᴡɴᴇʀ')}</b>\n"
    f"/broadcast — {sc('ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ')}\n\n"
    f"<i>{sc('ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴅʀᴀɢᴏɴʙʏᴛᴇ ɴᴇᴛᴡᴏʀᴋ')}</i>"
)


@app.on_message(filters.command("help") & ~filters.bot)
async def help_cmd(_, m: Message):
    await m.reply_text(
        HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(sc("ꜱᴜᴘᴘᴏʀᴛ"), url=SUPPORT_CHAT_LINK),
                InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url=f"https://t.me/{UPDATES_CHANNEL}"),
            ]
        ]),
    )


@app.on_callback_query(filters.regex("^help$"))
async def help_cb(_, q):
    await q.message.edit_text(
        HELP_TEXT,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="back")]
        ]),
    )
    await q.answer()


@app.on_callback_query(filters.regex("^back$"))
async def back_cb(_, q):
    await q.message.delete()
    await q.message.reply_photo(
        photo=random.choice(IMG),
        caption=START_TEXT,
        reply_markup=start_btns(),
    )
    await q.answer()


@app.on_message(filters.command("id"))
async def id_cmd(_, m: Message):
    text = (
        f"<b>{sc('ʏᴏᴜʀ ɪᴅ')}</b> : <code>{m.from_user.id}</code>\n"
        f"<b>{sc('ᴄʜᴀᴛ ɪᴅ')}</b> : <code>{m.chat.id}</code>"
    )
    if m.reply_to_message and m.reply_to_message.from_user:
        text += f"\n<b>{sc('ʀᴇᴘʟɪᴇᴅ')}</b> : <code>{m.reply_to_message.from_user.id}</code>"
    await m.reply_text(text)
