from __future__ import annotations
# © 2026 DragonByte Network | @flexyy
# Telegram PosterFORGE — layouts + caption + inline controls

import io
import os
import tempfile
from typing import Any

import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
    Message,
)

from config import TMDB_API_KEY
from Cyra import app
from Cyra.helpers import sc
from Cyra.modules.tmdb import tmdb_get

IMG_BASE = "https://image.tmdb.org/t/p"

# user_id -> studio state
SESSIONS: dict[int, dict[str, Any]] = {}

DEFAULTS = {
    "layout": "classic",       # classic | hero | minimal
    "quality": "1080p",        # 720p | 1080p | 4K
    "audio": "Hindi",          # Hindi | English | Dual
    "status": "Completed",     # Completed | Continuing | Upcoming
    "pixels": "1080p",
    "channel": "DragonByte",
    "show_overview": True,
}


def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _fit(text: str, draw: ImageDraw.ImageDraw, font, max_w: int) -> str:
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


def _wrap(text: str, draw: ImageDraw.ImageDraw, font, max_w: int, max_lines: int = 4) -> list[str]:
    words = (text or "").split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and words:
        lines[-1] = _fit(lines[-1], draw, font, max_w)
    return lines


async def fetch_bytes(url: str) -> bytes:
    if not url:
        return None
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=25) as r:
                if r.status == 200:
                    return await r.read()
    except Exception:
        return None
    return None


async def load_details(media_type: str, tmdb_id: int) -> dict:
    path = f"/{media_type}/{tmdb_id}"
    data = await tmdb_get(path, {
        "append_to_response": "images,external_ids",
        "include_image_language": "en,null,hi",
    })
    if not data:
        return None
    is_tv = media_type == "tv"
    title = data.get("name") if is_tv else data.get("title")
    date = data.get("first_air_date") if is_tv else data.get("release_date")
    year = (date or "")[:4]
    genres = ", ".join(g["name"] for g in (data.get("genres") or [])[:4])
    overview = (data.get("overview") or "")[:400]
    rating = round(float(data.get("vote_average") or 0), 1)
    poster = data.get("poster_path")
    backdrop = data.get("backdrop_path")
    runtime = None
    episodes = None
    if is_tv:
        episodes = data.get("number_of_episodes")
        runtime = (data.get("episode_run_time") or [None])[0]
    else:
        runtime = data.get("runtime")
    return {
        "id": tmdb_id,
        "type": media_type,
        "title": title or "Unknown",
        "year": year,
        "genres": genres,
        "overview": overview,
        "rating": rating,
        "poster": f"{IMG_BASE}/w780{poster}" if poster else None,
        "backdrop": f"{IMG_BASE}/w1280{backdrop}" if backdrop else None,
        "runtime": runtime,
        "episodes": episodes,
        "link": f"https://www.themoviedb.org/{media_type}/{tmdb_id}",
    }


def build_caption(d: dict, s: dict) -> str:
    title = d["title"]
    year = d["year"]
    lines = [
        f"🎬 {title} ({year})",
        "╭───────────────────",
    ]
    if s.get("status"):
        lines.append(f"➥ Status: {s['status']}")
    if d.get("episodes"):
        lines.append(f"➥ Episodes: {d['episodes']}")
    if d.get("rating"):
        lines.append(f"➥ Ratings: {d['rating']} TMDb")
    lines.append(f"➥ Pixels: {s.get('quality') or s.get('pixels') or '1080p'}")
    lines.append(f"➥ Audio: {s.get('audio') or 'Hindi'}")
    lines.append("├───────────────────")
    if d.get("genres"):
        lines.append(f"➥ Genres: {d['genres']}")
    lines.append("╰───────────────────")
    if s.get("show_overview") and d.get("overview"):
        lines.append(f"≡ {d['overview'][:220]}")
    ch = s.get("channel") or "DragonByte"
    lines.append("╭───────────────────")
    lines.append(f"➥ Powered by: {ch}")
    lines.append("╰───────────────────")
    # hashtags
    tags = ["#" + g.strip().replace(" ", "") for g in (d.get("genres") or "").split(",") if g.strip()]
    tags.append("#PosterFORGE")
    lines.append(" ".join(tags[:6]))
    return "\n".join(lines)


def render_poster(d: dict, s: dict, poster_bytes: bytes, back_bytes: bytes) -> bytes:
    layout = s.get("layout") or "classic"
    q = s.get("quality") or "1080p"
    sizes = {"720p": (720, 1280), "1080p": (1080, 1920), "4K": (1440, 2560)}
    # landscape-ish for classic/hero
    if layout in ("classic", "hero"):
        sizes = {"720p": (1280, 720), "1080p": (1920, 1080), "4K": (2560, 1440)}
    W, H = sizes.get(q, (1920, 1080))

    base_img = None
    raw = back_bytes or poster_bytes
    if raw:
        try:
            base_img = Image.open(io.BytesIO(raw)).convert("RGB")
        except Exception:
            base_img = None
    if base_img is None:
        base_img = Image.new("RGB", (W, H), (20, 20, 28))

    # cover resize
    img = base_img.copy()
    img = ImageEnhance.Brightness(img).enhance(0.75)
    img = img.resize((W, H), Image.Resampling.LANCZOS)
    # blur overlay layer
    blur = img.filter(ImageFilter.GaussianBlur(24))
    canvas = Image.new("RGB", (W, H))
    canvas.paste(blur, (0, 0))
    # dark gradient
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        a = int(180 * (y / H) ** 1.2) + 40
        od.line([(0, y), (W, y)], fill=(0, 0, 0, min(a, 210)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    # poster card on left (classic)
    pad = int(W * 0.04)
    if poster_bytes and layout != "minimal":
        try:
            pimg = Image.open(io.BytesIO(poster_bytes)).convert("RGB")
            ph = int(H * 0.72)
            pw = int(ph * 2 / 3)
            pimg = pimg.resize((pw, ph), Image.Resampling.LANCZOS)
            px, py = pad, (H - ph) // 2
            # shadow
            shadow = Image.new("RGBA", (pw + 20, ph + 20), (0, 0, 0, 0))
            sd = ImageDraw.Draw(shadow)
            sd.rounded_rectangle([0, 0, pw + 18, ph + 18], radius=16, fill=(0, 0, 0, 120))
            canvas.paste(shadow, (px - 6, py - 4), shadow)
            # rounded paste approx
            mask = Image.new("L", (pw, ph), 0)
            md = ImageDraw.Draw(mask)
            md.rounded_rectangle([0, 0, pw, ph], radius=14, fill=255)
            canvas.paste(pimg, (px, py), mask)
            text_x = px + pw + pad
        except Exception:
            text_x = pad
    else:
        text_x = pad

    max_tw = W - text_x - pad

    title_font = _font(max(28, W // 28), bold=True)
    meta_font = _font(max(18, W // 55))
    small_font = _font(max(16, W // 60))
    brand_font = _font(max(16, W // 58), bold=True)

    y = int(H * 0.18) if layout == "hero" else int(H * 0.22)
    title = d["title"]
    for line in _wrap(title, draw, title_font, max_tw, 2):
        draw.text((text_x, y), line, font=title_font, fill=(255, 255, 255))
        y += title_font.size + 8

    meta = f"{d.get('year') or ''}  ·  ⭐ {d.get('rating') or '—'}  ·  {s.get('quality') or '1080p'}"
    draw.text((text_x, y + 6), meta, font=meta_font, fill=(200, 210, 230))
    y += meta_font.size + 28

    chips = [
        s.get("status") or "Completed",
        s.get("audio") or "Hindi",
        d.get("genres", "").split(",")[0].strip() if d.get("genres") else "",
    ]
    cx = text_x
    for chip in chips:
        if not chip:
            continue
        tw = draw.textlength(chip, font=small_font) + 24
        draw.rounded_rectangle([cx, y, cx + tw, y + small_font.size + 14], radius=10, fill=(255, 255, 255, 40))
        # solid chip
        draw.rounded_rectangle([cx, y, cx + tw, y + small_font.size + 14], radius=10, fill=(40, 48, 70))
        draw.text((cx + 12, y + 6), chip, font=small_font, fill=(230, 235, 255))
        cx += tw + 10
    y += small_font.size + 36

    if s.get("show_overview") and d.get("overview") and layout != "minimal":
        for line in _wrap(d["overview"], draw, small_font, max_tw, 4):
            draw.text((text_x, y), line, font=small_font, fill=(180, 190, 210))
            y += small_font.size + 6

    # brand bar
    ch = s.get("channel") or "DragonByte"
    bar_h = int(H * 0.07)
    draw.rectangle([0, H - bar_h, W, H], fill=(12, 14, 22))
    brand = f"ꓚʏ፝֟፝֟ʀᴀ  ×  {ch}  ·  PosterFORGE"
    bw = draw.textlength(brand, font=brand_font)
    draw.text(((W - bw) / 2, H - bar_h + (bar_h - brand_font.size) / 2), brand, font=brand_font, fill=(160, 175, 210))

    buf = io.BytesIO()
    canvas.save(buf, format="JPEG", quality=92)
    buf.seek(0)
    return buf.read()


def studio_keyboard(s: dict) -> InlineKeyboardMarkup:
    layout = s.get("layout", "classic")
    quality = s.get("quality", "1080p")
    audio = s.get("audio", "Hindi")
    status = s.get("status", "Completed")
    ov = s.get("show_overview", True)

    def mark(cur, val):
        return "• " + val if cur == val else val

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(sc(mark(layout, "classic")), callback_data="pf:set:layout:classic"),
            InlineKeyboardButton(sc(mark(layout, "hero")), callback_data="pf:set:layout:hero"),
            InlineKeyboardButton(sc(mark(layout, "minimal")), callback_data="pf:set:layout:minimal"),
        ],
        [
            InlineKeyboardButton(sc(mark(quality, "720p")), callback_data="pf:set:quality:720p"),
            InlineKeyboardButton(sc(mark(quality, "1080p")), callback_data="pf:set:quality:1080p"),
            InlineKeyboardButton(sc(mark(quality, "4K")), callback_data="pf:set:quality:4K"),
        ],
        [
            InlineKeyboardButton(sc(mark(audio, "Hindi")), callback_data="pf:set:audio:Hindi"),
            InlineKeyboardButton(sc(mark(audio, "English")), callback_data="pf:set:audio:English"),
            InlineKeyboardButton(sc(mark(audio, "Dual")), callback_data="pf:set:audio:Dual"),
        ],
        [
            InlineKeyboardButton(sc(mark(status, "Completed")), callback_data="pf:set:status:Completed"),
            InlineKeyboardButton(sc(mark(status, "Continuing")), callback_data="pf:set:status:Continuing"),
            InlineKeyboardButton(sc(mark(status, "Upcoming")), callback_data="pf:set:status:Upcoming"),
        ],
        [
            InlineKeyboardButton(
                sc("overview ᴏɴ" if ov else "overview ᴏꜰꜰ"),
                callback_data="pf:set:overview:toggle",
            ),
            InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), callback_data="pf:set:channel:ask"),
        ],
        [
            InlineKeyboardButton(sc("🎨 ɢᴇɴᴇʀᴀᴛᴇ ᴘᴏꜱᴛᴇʀ"), callback_data="pf:gen"),
            InlineKeyboardButton(sc("📝 ᴄᴀᴘᴛɪᴏɴ"), callback_data="pf:cap"),
        ],
        [InlineKeyboardButton(sc("ᴄʟᴏꜱᴇ"), callback_data="pf:close")],
    ])


async def open_studio(cq: CallbackQuery, media_type: str, tmdb_id: int):
    await cq.answer(sc("ʟᴏᴀᴅɪɴɢ..."))
    d = await load_details(media_type, tmdb_id)
    if not d:
        return await cq.message.edit_text(sc("ᴅᴇᴛᴀɪʟꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ"))

    uid = cq.from_user.id
    state = {**DEFAULTS, "data": d}
    SESSIONS[uid] = state

    poster_b = await fetch_bytes(d.get("poster"))
    thumb = d.get("poster") or d.get("backdrop")
    cap = (
        f"<b>{d['title']}</b> ({d['year']})\n"
        f"{'🎬' if d['type']=='movie' else '📺'} · ⭐ <code>{d['rating']}</code>\n\n"
        f"<i>{sc('ɴᴇᴇᴄʜᴇ ꜱᴇ ᴏᴘᴛɪᴏɴꜱ ᴄʜᴀɴɢᴇ ᴋᴀʀᴏ · ᴘʜɪʀ ɢᴇɴᴇʀᴀᴛᴇ')}</i>"
    )
    kb = studio_keyboard(state)
    try:
        if thumb:
            await cq.message.delete()
            await app.send_photo(
                cq.message.chat.id,
                photo=thumb,
                caption=cap,
                reply_markup=kb,
            )
        else:
            await cq.message.edit_text(cap, reply_markup=kb)
    except Exception:
        await cq.message.reply_text(cap, reply_markup=kb)


@app.on_callback_query(filters.regex(r"^pf:pick:(movie|tv):(\d+)$"))
async def pf_pick(_, cq: CallbackQuery):
    parts = cq.data.split(":")
    await open_studio(cq, parts[2], int(parts[3]))


@app.on_callback_query(filters.regex(r"^pf:set:"))
async def pf_set(_, cq: CallbackQuery):
    uid = cq.from_user.id
    state = SESSIONS.get(uid)
    if not state:
        return await cq.answer(sc("ꜱᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ · /tmdb ꜱᴇ ᴘʜɪʀ ꜱᴇʟᴇᴄᴛ ᴋᴀʀᴏ"), show_alert=True)

    # pf:set:key:value
    _, _, key, val = cq.data.split(":", 3)
    if key == "overview":
        state["show_overview"] = not state.get("show_overview", True)
    elif key == "channel":
        await cq.answer()
        await cq.message.reply_text(
            f"{sc('ɴᴀʏᴀ ᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇ ʙʜᴇᴊᴏ')}\n"
            f"<code>/setchannel DragonByte</code>"
        )
        return
    else:
        state[key] = val
        if key == "quality":
            state["pixels"] = val

    SESSIONS[uid] = state
    try:
        await cq.message.edit_reply_markup(reply_markup=studio_keyboard(state))
    except Exception:
        pass
    await cq.answer(sc("ᴜᴘᴅᴀᴛᴇᴅ"))


@app.on_message(filters.command("setchannel"))
async def set_channel(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"<code>/setchannel DragonByte</code>")
    name = " ".join(m.command[1:]).strip()[:32]
    uid = m.from_user.id
    state = SESSIONS.get(uid)
    if not state:
        return await m.reply_text(sc("ᴘᴇʜʟᴇ /tmdb ꜱᴇ ᴛɪᴛʟᴇ ꜱᴇʟᴇᴄᴛ ᴋᴀʀᴏ"))
    state["channel"] = name
    SESSIONS[uid] = state
    await m.reply_text(f"✅ {sc('ᴄʜᴀɴɴᴇʟ')} → <b>{name}</b>\n{sc('ᴀʙ ɢᴇɴᴇʀᴀᴛᴇ ᴅᴜʙᴀʀᴀ ᴅᴀʙᴀᴏ')}")


@app.on_callback_query(filters.regex(r"^pf:gen$"))
async def pf_gen(_, cq: CallbackQuery):
    uid = cq.from_user.id
    state = SESSIONS.get(uid)
    if not state or "data" not in state:
        return await cq.answer(sc("ꜱᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ"), show_alert=True)

    await cq.answer(sc("ʀᴇɴᴅᴇʀɪɴɢ..."))
    d = state["data"]
    wait = await cq.message.reply_text(f"🎨 {sc('ᴘᴏꜱᴛᴇʀ ʙᴀɴ ᴠᴀʜᴀ ʜᴀɪ')}...")

    poster_b = await fetch_bytes(d.get("poster"))
    back_b = await fetch_bytes(d.get("backdrop"))
    try:
        jpg = render_poster(d, state, poster_b, back_b)
        caption = build_caption(d, state)
        await cq.message.reply_photo(
            photo=io.BytesIO(jpg),
            caption=caption[:1024],
        )
        await wait.delete()
    except Exception as e:
        await wait.edit_text(f"❌ <code>{str(e)[:200]}</code>")


@app.on_callback_query(filters.regex(r"^pf:cap$"))
async def pf_cap(_, cq: CallbackQuery):
    uid = cq.from_user.id
    state = SESSIONS.get(uid)
    if not state or "data" not in state:
        return await cq.answer(sc("ꜱᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ"), show_alert=True)
    cap = build_caption(state["data"], state)
    await cq.answer()
    await cq.message.reply_text(f"<b>{sc('ᴄᴀᴘᴛɪᴏɴ')}</b>\n\n<code>{cap}</code>")


@app.on_callback_query(filters.regex(r"^pf:close$"))
async def pf_close(_, cq: CallbackQuery):
    SESSIONS.pop(cq.from_user.id, None)
    await cq.answer(sc("ᴄʟᴏꜱᴇᴅ"))
    try:
        await cq.message.delete()
    except Exception:
        pass


@app.on_message(filters.command(["poster", "posterforge"]))
async def poster_help(_, m: Message):
    await m.reply_text(
        f"<b>{sc('ᴘᴏꜱᴛᴇʀꜰᴏʀɢᴇ')}</b>\n\n"
        f"1. <code>/tmdb inception</code>\n"
        f"2. {sc('ʀᴇꜱᴜʟᴛ ꜱᴇʟᴇᴄᴛ ᴋᴀʀᴏ')}\n"
        f"3. {sc('ʟᴀʏᴏᴜᴛ / ǫᴜᴀʟɪᴛʏ / ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇ ᴋᴀʀᴏ')}\n"
        f"4. <b>{sc('ɢᴇɴᴇʀᴀᴛᴇ ᴘᴏꜱᴛᴇʀ')}</b>\n\n"
        f"<code>/setchannel YourName</code> — {sc('ᴘᴏᴡᴇʀᴇᴅ ʙʏ ɴᴀᴍᴇ')}\n\n"
        f"<i>{sc('ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴅʀᴀɢᴏɴʙʏᴛᴇ ɴᴇᴛᴡᴏʀᴋ')}</i>"
    )
