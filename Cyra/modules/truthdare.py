# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc

TRUTHS = [
    "What is your most embarrassing memory?",
    "Who was your first crush in this group?",
    "What secret have you never told anyone here?",
    "Which member do you text the most?",
    "Have you ever stalked someone from this chat?",
    "What is the weirdest dream you remember?",
    "Who would you want as a partner on a deserted island?",
    "What is one thing you regret saying online?",
]

DARES = [
    "Send a voice note saying you love this group.",
    "Change your group nickname for 10 minutes.",
    "Compliment the person above you.",
    "Send your last emoji-only message style here.",
    "Type with your elbow for one message.",
    "Post a random selfie sticker if you have one.",
    "Say good morning in 3 languages.",
    "Tag 2 admins and thank them.",
]


@app.on_message(filters.command(["truth", "t"]))
async def truth_cmd(_, m: Message):
    await m.reply_text(f"🔵 <b>{sc('ᴛʀᴜᴛʜ')}</b>\n\n{random.choice(TRUTHS)}")


@app.on_message(filters.command(["dare", "d"]))
async def dare_cmd(_, m: Message):
    await m.reply_text(f"🔴 <b>{sc('ᴅᴀʀᴇ')}</b>\n\n{random.choice(DARES)}")


@app.on_message(filters.command(["tod", "truthordare"]))
async def tod_cmd(_, m: Message):
    if random.random() < 0.5:
        await truth_cmd(_, m)
    else:
        await dare_cmd(_, m)
