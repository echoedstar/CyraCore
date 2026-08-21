# © 2026 DragonByte Network | @flexyy
# Pinterest photos — works without pinscrape (built-in fetch)

from __future__ import annotations

import asyncio
import json
import re
from urllib.parse import quote

import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.enums import ChatAction

from Cyra import app
from Cyra.helpers import sc

# optional — used only if installed
try:
    from pinscrape import Pinterest as PinLib
except Exception:
    PinLib = None


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pinterest.com/",
    "X-Requested-With": "XMLHttpRequest",
}


async def fetch_pin_urls(query: str, limit: int = 12) -> list[str]:
    """Fetch image URLs from Pinterest search (no pinscrape needed)."""
    urls: list[str] = []
    q = quote(query)
    api = (
        "https://www.pinterest.com/resource/BaseSearchResource/get/"
        f"?source_url=/search/pins/?q={q}"
        f"&data={quote(json.dumps({'options': {'query': query, 'scope': 'pins', 'page_size': limit}}))}"
    )
    timeout = aiohttp.ClientTimeout(total=25)
    async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
        # primary: resource API
        try:
            async with session.get(api) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    results = (
                        data.get("resource_response", {})
                        .get("data", {})
                        .get("results", [])
                    )
                    for item in results:
                        img = None
                        if isinstance(item, dict):
                            images = item.get("images") or {}
                            for key in ("orig", "originals", "736x", "564x", "474x"):
                                block = images.get(key)
                                if isinstance(block, dict) and block.get("url"):
                                    img = block["url"]
                                    break
                                if isinstance(block, list) and block:
                                    img = block[0].get("url")
                                    break
                        if img and img not in urls:
                            urls.append(img)
                        if len(urls) >= limit:
                            return urls[:limit]
        except Exception:
            pass

        # fallback: HTML page scrape
        try:
            page = f"https://www.pinterest.com/search/pins/?q={q}"
            async with session.get(page) as resp:
                html = await resp.text()
            # image CDN urls
            found = re.findall(
                r"https://i\.pinimg\.com/[^\"'\s]+?\.(?:jpg|jpeg|png|webp)",
                html,
                flags=re.I,
            )
            for u in found:
                # prefer larger variants
                u2 = re.sub(r"/\d+x/", "/736x/", u)
                if u2 not in urls:
                    urls.append(u2)
                if len(urls) >= limit:
                    break
        except Exception:
            pass

    return urls[:limit]


def fetch_with_pinscrape(query: str, limit: int = 10) -> list[str]:
    """Optional path if pinscrape is installed."""
    if PinLib is None:
        return []
    try:
        p = PinLib(proxies={}, sleep_time=1)
        return list(p.search(query, limit) or [])[:limit]
    except Exception:
        return []


@app.on_message(filters.command(["pinterest", "pin", "pins"]))
async def pinterest_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(
            f"<b>{sc('usage')}</b>\n<code>/pinterest cute cats</code>"
        )

    query = " ".join(m.command[1:]).strip()
    status = await m.reply_text(
        f"<b>{sc('searching')}</b> <code>{query}</code>\n{sc('please wait...')}"
    )

    try:
        await app.send_chat_action(m.chat.id, ChatAction.UPLOAD_PHOTO)
        loop = asyncio.get_event_loop()

        # 1) try built-in (no install needed)
        urls = await fetch_pin_urls(query, 12)

        # 2) optional pinscrape backup
        if len(urls) < 3 and PinLib is not None:
            extra = await loop.run_in_executor(None, fetch_with_pinscrape, query, 10)
            for u in extra:
                if u not in urls:
                    urls.append(u)

        urls = urls[:10]
        if not urls:
            return await status.edit_text(sc("no images found — try another query"))

        await status.edit_text(
            f"{sc('found')} <b>{len(urls)}</b> · {sc('sending...')}"
        )

        # send as media group using URLs directly (no disk)
        media = []
        for i, url in enumerate(urls):
            cap = (
                f"<b>{query}</b>\n"
                f"<i>{sc('cyra x pinterest')}</i>"
                if i == 0
                else None
            )
            media.append(InputMediaPhoto(media=url, caption=cap))

        await m.reply_media_group(media)
        await status.delete()
    except Exception as e:
        await status.edit_text(f"<code>{str(e)[:200]}</code>")
