# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc


@app.on_message(filters.command(["reverse", "rev"]))
async def reverse_cmd(_, m: Message):
    text = None
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    elif len(m.command) > 1:
        text = m.text.split(None, 1)[1]
    if not text:
        return await m.reply_text(f"<code>/reverse hello</code>")
    await m.reply_text(text[::-1])


@app.on_message(filters.command(["shout"]))
async def shout_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"<code>/shout cyra</code>")
    word = m.command[1][:20]
    lines = []
    for i, ch in enumerate(word):
        lines.append((" " * i) + " ".join(word[i:]).upper())
    await m.reply_text(f"<code>{chr(10).join(lines)}</code>")


@app.on_message(filters.command(["say", "echo"]))
async def say_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"<code>/say hello group</code>")
    text = m.text.split(None, 1)[1]
    await m.reply_text(text)


@app.on_message(filters.command(["bonk"]))
async def bonk_cmd(_, m: Message):
    target = m.reply_to_message.from_user.mention if m.reply_to_message else sc("ꜱᴏᴍᴇᴏɴᴇ")
    await m.reply_text(f"🔨 {m.from_user.mention} {sc('ʙᴏɴᴋᴇᴅ')} {target}")


@app.on_message(filters.command(["hug"]))
async def hug_cmd(_, m: Message):
    target = m.reply_to_message.from_user.mention if m.reply_to_message else sc("ᴛʜᴇ ɢʀᴏᴜᴘ")
    await m.reply_text(f"🤗 {m.from_user.mention} {sc('ʜᴜɢꜱ')} {target}")


@app.on_message(filters.command(["pat"]))
async def pat_cmd(_, m: Message):
    target = m.reply_to_message.from_user.mention if m.reply_to_message else sc("ʏᴏᴜ")
    await m.reply_text(f"♡ {m.from_user.mention} {sc('ᴘᴀᴛꜱ')} {target}")
