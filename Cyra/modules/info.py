# © 2026 DragonByte Network | @flexyy

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from Cyra import app
from Cyra.helpers import sc


@app.on_message(filters.command(["info", "whois", "userinfo"]))
async def info_cmd(_, m: Message):
    user = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    text = (
        f"👤 <b>{sc('ᴜꜱᴇʀ ɪɴꜰᴏ')}</b>\n\n"
        f"• {sc('ɴᴀᴍᴇ')}: {user.mention}\n"
        f"• {sc('ɪᴅ')}: <code>{user.id}</code>\n"
        f"• {sc('ᴜꜱᴇʀɴᴀᴍᴇ')}: @{user.username if user.username else '—'}\n"
        f"• {sc('ᴘʀᴇᴍɪᴜᴍ')}: {'✅' if user.is_premium else '❌'}\n"
        f"• DC: <code>{user.dc_id or '—'}</code>"
    )
    await m.reply_text(text)


@app.on_message(filters.command(["chatinfo", "groupinfo", "ginfo"]))
async def chatinfo_cmd(_, m: Message):
    c = m.chat
    text = (
        f"💬 <b>{sc('ᴄʜᴀᴛ ɪɴꜰᴏ')}</b>\n\n"
        f"• {sc('ᴛɪᴛʟᴇ')}: {c.title or 'PM'}\n"
        f"• {sc('ɪᴅ')}: <code>{c.id}</code>\n"
        f"• {sc('ᴛʏᴘᴇ')}: <code>{c.type}</code>\n"
        f"• {sc('ᴜꜱᴇʀɴᴀᴍᴇ')}: @{c.username if c.username else '—'}"
    )
    if c.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        try:
            full = await app.get_chat(c.id)
            text += f"\n• {sc('ᴍᴇᴍʙᴇʀꜱ')}: <code>{full.members_count or '—'}</code>"
        except Exception:
            pass
    await m.reply_text(text)


@app.on_message(filters.command(["admins", "adminlist"]))
async def admins_cmd(_, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        return await m.reply_text(sc("ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘꜱ"))
    lines = [f"🛡 <b>{sc('ᴀᴅᴍɪɴꜱ')}</b>\n"]
    try:
        async for adm in app.get_chat_members(m.chat.id, filter="administrators"):
            if adm.user.is_deleted:
                continue
            lines.append(f"• {adm.user.mention}")
        await m.reply_text("\n".join(lines[:40]))
    except Exception:
        await m.reply_text(sc("ᴄᴀɴᴛ ꜰᴇᴛᴄʜ ᴀᴅᴍɪɴꜱ"))
