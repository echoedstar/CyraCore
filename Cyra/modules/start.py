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
    f"<b>{sc('ᴄᴏʀᴇ')}</b>\n"
    f"/start /help /ping /stats /id\n\n"
    f"<b>{sc('ᴍᴇᴅɪᴀ')}</b>\n"
    f"/pinterest /pin — {sc('ᴘɪɴᴛᴇʀᴇꜱᴛ ᴘʜᴏᴛᴏꜱ')}\n"
    f"/tmdb — {sc('ᴍᴏᴠɪᴇ ꜱᴇᴀʀᴄʜ + ᴘᴏꜱᴛᴇʀ')}\n"
    f"/poster — {sc('ᴘᴏꜱᴛᴇʀꜰᴏʀɢᴇ ʜᴇʟᴘ')}\n\n"
    f"<b>{sc('ɢʀᴏᴜᴘ ꜰᴜɴ')}</b>\n"
    f"/truth /dare /tod\n"
    f"/joke /quote /roast\n"
    f"/ship /couple /gayrate /love\n"
    f"/dice /coin /choose /decide\n"
    f"/hug /pat /bonk /meme\n"
    f"/reverse /shout /emojify /password\n\n"
    f"<b>{sc('ɢʀᴏᴜᴘ ᴛᴏᴏʟꜱ')}</b>\n"
    f"/info /chatinfo /admins\n"
    f"/warn /warns /delwarn /del\n\n"
    f"<b>{sc('ᴏᴡɴᴇʀ')}</b>\n"
    f"/broadcast\n\n"
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
