# © 2026 DragonByte Network | @flexyy

import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import TMDB_API_KEY
from Cyra import app
from Cyra.helpers import sc

BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"


@app.on_message(filters.command(["tmdb", "movie", "movies"]))
async def tmdb_cmd(_, m: Message):
    if not TMDB_API_KEY:
        return await m.reply_text(
            f"{sc('ᴛᴍᴅʙ_ᴀᴘɪ_ᴋᴇʏ ᴍɪꜱꜱɪɴɢ ɪɴ .ᴇɴᴠ')}\n"
            f"<i>get free key → themoviedb.org</i>"
        )

    if len(m.command) < 2:
        return await m.reply_text(
            f"<b>{sc('ᴜꜱᴀɢᴇ')}</b>\n<code>/tmdb inception</code>"
        )

    query = " ".join(m.command[1:]).strip()
    status = await m.reply_text(f"🎬 {sc('ꜱᴇᴀʀᴄʜɪɴɢ')} <code>{query}</code>...")

    url = f"{BASE}/search/multi"
    params = {"api_key": TMDB_API_KEY, "query": query, "language": "en-US", "page": 1}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=15) as resp:
                data = await resp.json()

        results = data.get("results") or []
        # prefer movie/tv with poster
        results = [r for r in results if r.get("media_type") in ("movie", "tv")][:5]
        if not results:
            return await status.edit_text(sc("ɴᴏ ʀᴇꜱᴜʟᴛꜱ"))

        await status.delete()
        for r in results[:3]:
            title = r.get("title") or r.get("name") or "—"
            year = (r.get("release_date") or r.get("first_air_date") or "")[:4]
            overview = (r.get("overview") or sc("ɴᴏ ᴏᴠᴇʀᴠɪᴇᴡ"))[:280]
            rating = r.get("vote_average") or 0
            mtype = "🎬 ᴍᴏᴠɪᴇ" if r.get("media_type") == "movie" else "📺 ꜱᴇʀɪᴇꜱ"
            poster = r.get("poster_path")
            photo = f"{IMG_BASE}{poster}" if poster else None
            tmdb_id = r.get("id")
            link = f"https://www.themoviedb.org/{r.get('media_type')}/{tmdb_id}"

            cap = (
                f"<b>{title}</b> ({year})\n"
                f"{mtype} · ⭐ <code>{rating}</code>\n\n"
                f"<i>{overview}</i>"
            )
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton(sc("ᴛᴍᴅʙ"), url=link)]
            ])
            if photo:
                await m.reply_photo(photo=photo, caption=cap, reply_markup=btn)
            else:
                await m.reply_text(cap, reply_markup=btn)
    except Exception as e:
        await status.edit_text(f"❌ <code>{str(e)[:180]}</code>")
