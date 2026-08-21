# © 2026 DragonByte Network | @flexyy

from collections import defaultdict
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatType
from Cyra import app
from Cyra.helpers import sc

# chat_id -> user_id -> count
WARNS: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))


async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        m = await app.get_chat_member(chat_id, user_id)
        return m.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except Exception:
        return False


@app.on_message(filters.command(["warn"]) & filters.group)
async def warn_cmd(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text(sc("ᴀᴅᴍɪɴꜱ ᴏɴʟʏ"))
    if not m.reply_to_message:
        return await m.reply_text(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ"))
    target = m.reply_to_message.from_user
    if target.id == m.from_user.id:
        return await m.reply_text(sc("ᴄᴀɴᴛ ᴡᴀʀɴ ʏᴏᴜʀꜱᴇʟꜰ"))
    WARNS[m.chat.id][target.id] += 1
    count = WARNS[m.chat.id][target.id]
    reason = m.text.split(None, 1)[1] if len(m.command) > 1 else "—"
    await m.reply_text(
        f"⚠️ <b>{sc('ᴡᴀʀɴ')}</b> {target.mention}\n"
        f"{sc('ᴄᴏᴜɴᴛ')}: <code>{count}/3</code>\n"
        f"{sc('ʀᴇᴀꜱᴏɴ')}: {reason}"
    )


@app.on_message(filters.command(["warns"]) & filters.group)
async def warns_cmd(_, m: Message):
    target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    count = WARNS[m.chat.id].get(target.id, 0)
    await m.reply_text(f"⚠️ {target.mention}: <code>{count}</code> {sc('ᴡᴀʀɴꜱ')}")


@app.on_message(filters.command(["delwarn", "resetwarn"]) & filters.group)
async def delwarn_cmd(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text(sc("ᴀᴅᴍɪɴꜱ ᴏɴʟʏ"))
    if not m.reply_to_message:
        return await m.reply_text(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ"))
    target = m.reply_to_message.from_user
    WARNS[m.chat.id][target.id] = 0
    await m.reply_text(f"✅ {sc('ᴡᴀʀɴꜱ ʀᴇꜱᴇᴛ ꜰᴏʀ')} {target.mention}")


@app.on_message(filters.command(["del", "delete"]) & filters.group)
async def del_cmd(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return
    if m.reply_to_message:
        try:
            await m.reply_to_message.delete()
            await m.delete()
        except Exception:
            await m.reply_text(sc("ᴄᴀɴᴛ ᴅᴇʟᴇᴛᴇ"))
