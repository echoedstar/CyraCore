# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc

ROASTS = [
    "{name}'s WiFi signal is stronger than their personality.",
    "{name} brings everyone so much joy… when they leave the chat.",
    "{name} is proof that even evolution takes coffee breaks.",
    "If laziness was an Olympic sport, {name} would still come late.",
    "{name}'s secrets are safe with me. I never listen anyway.",
    "{name} has a face for radio and a voice for silent mode.",
    "Somewhere, a tree is working hard so {name} can act this dense.",
    "{name} is not stupid — they just have bad luck thinking.",
    "I'd agree with {name}, but then we'd both be wrong.",
    "{name} is like a cloud: when they disappear, it's a beautiful day.",
]


@app.on_message(filters.command(["roast", "insult", "burn"]))
async def roast_cmd(_, m: Message):
    user = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    text = random.choice(ROASTS).format(name=user.first_name)
    await m.reply_text(f"🔥 <b>{sc('ʀᴏᴀꜱᴛ')}</b>\n\n{text}\n\n<i>{sc('ᴊᴜꜱᴛ ꜰᴏʀ ꜰᴜɴ')}</i>")
