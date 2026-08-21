# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc

QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Everything you can imagine is real.", "Pablo Picasso"),
    ("Happiness depends upon ourselves.", "Aristotle"),
    ("Turn your wounds into wisdom.", "Oprah Winfrey"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("Be yourself; everyone else is already taken.", "Oscar Wilde"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
]


@app.on_message(filters.command(["quote", "quotes", "quoteoftheday"]))
async def quote_cmd(_, m: Message):
    q, a = random.choice(QUOTES)
    await m.reply_text(f"💬 <b>{sc('ǫᴜᴏᴛᴇ')}</b>\n\n<i>“{q}”</i>\n— <b>{a}</b>")
