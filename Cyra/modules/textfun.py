# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc


@app.on_message(filters.command(["emojify"]))
async def emojify_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"<code>/emojify hello</code>")
    text = m.text.split(None, 1)[1]
    em = ["✨", "🔥", "💕", "🌟", "⚡", "🎀", "🌈"]
    out = " ".join(f"{random.choice(em)}{c}" for c in text if c != " ")
    await m.reply_text(out)


@app.on_message(filters.command(["password", "pwgen"]))
async def pw_cmd(_, m: Message):
    length = 12
    if len(m.command) > 1 and m.command[1].isdigit():
        length = max(6, min(32, int(m.command[1])))
    chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$"
    pw = "".join(random.choice(chars) for _ in range(length))
    await m.reply_text(f"🔑 <code>{pw}</code>")


@app.on_message(filters.command(["decide", "yesno"]))
async def decide_cmd(_, m: Message):
    await m.reply_text(f"🎱 <b>{random.choice(['Yes', 'No', 'Maybe', 'Absolutely', 'Nope'])}</b>")


@app.on_message(filters.command(["meme"]))
async def meme_cmd(_, m: Message):
    # light text memes without external API
    templates = [
        "When the group is dead and you drop a {x}",
        "Nobody:\nAbsolutely nobody:\n{x}: enters the chat",
        "POV: {x} just joined the group",
        "Teacher: where is your homework?\n{x}:",
    ]
    x = m.from_user.first_name
    if m.reply_to_message and m.reply_to_message.from_user:
        x = m.reply_to_message.from_user.first_name
    await m.reply_text(f"📸 <b>{sc('ᴍᴇᴍᴇ')}</b>\n\n{random.choice(templates).format(x=x)}")
