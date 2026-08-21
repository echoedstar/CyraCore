# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc


def bar(pct: int) -> str:
    filled = round(pct / 10)
    return "█" * filled + "░" * (10 - filled)


@app.on_message(filters.command(["ship", "shipping"]))
async def ship_cmd(_, m: Message):
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply_text(f"{sc('ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴜꜱᴇ')}\n<code>/ship @user1 @user2</code>")

    u1 = m.from_user
    u2 = m.reply_to_message.from_user if m.reply_to_message else None
    if len(m.command) >= 3:
        a, b = m.command[1], m.command[2]
        name1, name2 = a, b
    elif u2:
        name1, name2 = u1.first_name, u2.first_name
    else:
        name1, name2 = u1.first_name, m.command[1]

    pct = random.randint(1, 100)
    await m.reply_text(
        f"💘 <b>{sc('ꜱʜɪᴘ')}</b>\n\n"
        f"<b>{name1}</b> ➕ <b>{name2}</b>\n"
        f"{bar(pct)} <code>{pct}%</code>\n\n"
        f"<i>{sc('ᴄᴜᴛᴇ ᴄᴏᴜᴘʟᴇ') if pct > 70 else sc('ꜰʀɪᴇɴᴅꜱ ᴢᴏɴᴇ') if pct < 40 else sc('ᴍᴀʏʙᴇ...')}</i>"
    )


@app.on_message(filters.command(["couple", "couples"]))
async def couple_cmd(_, m: Message):
    if m.chat.type.name == "PRIVATE":
        return await m.reply_text(sc("ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘꜱ"))
    try:
        members = []
        async for mem in app.get_chat_members(m.chat.id, limit=50):
            if not mem.user.is_bot and not mem.user.is_deleted:
                members.append(mem.user)
        if len(members) < 2:
            return await m.reply_text(sc("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴍᴇᴍʙᴇʀꜱ"))
        a, b = random.sample(members, 2)
        await m.reply_text(
            f"💕 <b>{sc('ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ')}</b>\n\n"
            f"{a.mention} ➕ {b.mention}\n"
            f"<i>{sc('ᴄᴜᴛᴇ ʀɪɢʜᴛ?')}</i>"
        )
    except Exception:
        await m.reply_text(sc("ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ ᴛᴏ ᴘɪᴄᴋ ᴍᴇᴍʙᴇʀꜱ"))


@app.on_message(filters.command(["gayrate", "gay", "howgay"]))
async def gayrate_cmd(_, m: Message):
    user = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    pct = random.randint(0, 100)
    await m.reply_text(
        f"🏳️‍🌈 <b>{sc('ɢᴀʏ ʀᴀᴛᴇ')}</b>\n\n"
        f"{user.mention}\n{bar(pct)} <code>{pct}%</code>"
    )


@app.on_message(filters.command(["lovemeter", "love"]))
async def love_cmd(_, m: Message):
    user = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    pct = random.randint(1, 100)
    await m.reply_text(
        f"❤️ <b>{sc('ʟᴏᴠᴇ ᴍᴇᴛᴇʀ')}</b>\n\n"
        f"{user.mention}\n{bar(pct)} <code>{pct}%</code>"
    )
