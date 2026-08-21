# © 2026 DragonByte Network | @flexyy

import random
from pyrogram import filters
from pyrogram.types import Message
from Cyra import app
from Cyra.helpers import sc


@app.on_message(filters.command(["dice", "roll"]))
async def dice_cmd(_, m: Message):
    await m.reply_dice(emoji="🎲")


@app.on_message(filters.command(["coin", "flip"]))
async def coin_cmd(_, m: Message):
    side = random.choice(["Heads", "Tails"])
    await m.reply_text(f"🪙 <b>{sc('ᴄᴏɪɴ ꜰʟɪᴘ')}</b>\n\n<code>{side}</code>")


@app.on_message(filters.command(["choose", "pick", "select"]))
async def choose_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"<code>/choose pizza pasta burger</code>")
    opts = m.text.split(None, 1)[1].replace(",", " ").split()
    if len(opts) < 2:
        return await m.reply_text(sc("ɢɪᴠᴇ ᴀᴛ ʟᴇᴀꜱᴛ 2 ᴏᴘᴛɪᴏɴꜱ"))
    await m.reply_text(
        f"🎯 <b>{sc('ɪ ᴄʜᴏᴏꜱᴇ')}</b>\n\n<code>{random.choice(opts)}</code>"
    )


@app.on_message(filters.command(["toss"]))
async def toss_cmd(_, m: Message):
    await coin_cmd(_, m)
