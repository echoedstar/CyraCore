from __future__ import annotations
# © 2026 DragonByte Network | @flexyy

import io
import aiohttp
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from config import TMDB_API_KEY
from Cyra import app
from Cyra.helpers import sc

BASE = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p"


async def tmdb_get(path: str, params: dict = None):
    params = params or {}
    params["api_key"] = TMDB_API_KEY
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{BASE}{path}", params=params, timeout=20) as r:
            if r.status != 200:
                return None
            return await r.json()


@app.on_message(filters.command(["tmdb", "movie", "movies", "series"]))
async def tmdb_search(_, m: Message):
    if not TMDB_API_KEY:
        return await m.reply_text(sc("ᴛᴍᴅʙ ᴋᴇʏ ᴍɪꜱꜱɪɴɢ"))

    if len(m.command) < 2:
        return await m.reply_text(
            f"<b>{sc('ᴜꜱᴀɢᴇ')}</b>\n"
            f"<code>/tmdb inception</code>\n"
            f"<code>/tmdb breaking bad</code>"
        )

    q = " ".join(m.command[1:]).strip()
    st = await m.reply_text(f"{sc('ꜱᴇᴀʀᴄʜɪɴɢ')} <code>{q}</code>...")

    data = await tmdb_get("/search/multi", {"query": q, "include_adult": "false"})
    if not data or not data.get("results"):
        return await st.edit_text(sc("ɴᴏ ʀᴇꜱᴜʟᴛꜱ"))

    results = [
        r for r in data["results"]
        if r.get("media_type") in ("movie", "tv")
    ][:8]
    if not results:
        return await st.edit_text(sc("ɴᴏ ʀᴇꜱᴜʟᴛꜱ"))

    lines = [f"<b>{sc('ʀᴇꜱᴜʟᴛꜱ ꜰᴏʀ')}</b> <code>{q}</code>\n"]
    buttons = []
    for i, r in enumerate(results, 1):
        title = r.get("title") or r.get("name") or "?"
        year = (r.get("release_date") or r.get("first_air_date") or "")[:4]
        mtype = "[M]" if r["media_type"] == "movie" else "[S]"
        rating = r.get("vote_average") or 0
        lines.append(f"{i}. {mtype} <b>{title}</b> ({year}) · ⭐{rating:.1f}")
        buttons.append([
            InlineKeyboardButton(
                f"{mtype} {title[:28]}",
                callback_data=f"pf:pick:{r['media_type']}:{r['id']}",
            )
        ])

    await st.edit_text(
        "\n".join(lines) + f"\n\n<i>{sc('ᴘᴏꜱᴛᴇʀ ʙᴀɴᴀɴᴇ ᴋᴇ ʟɪʏᴇ ꜱᴇʟᴇᴄᴛ ᴋᴀʀᴏ')}</i>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
