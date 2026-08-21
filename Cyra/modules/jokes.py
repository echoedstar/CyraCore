# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my computer I needed a break… it froze.",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I asked my dog what's two minus two. He said nothing.",
    "Why did the mobile phone go to school? To improve its reception.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I would tell you a UDP joke… but you might not get it.",
    "There are 10 kinds of people: those who understand binary and those who don't.",
]


@app.on_message(filters.command(["joke", "jokes", "funny"]))
async def joke_cmd(_, m: Message):
    await m.reply_text(f"😂 <b>{sc('ᴊᴏᴋᴇ')}</b>\n\n{random.choice(JOKES)}")
