# © 2026 DragonByte Network | @flexyy
# PosterFORGE for Telegram — landscape / hero / cinema + caption templates

from __future__ import annotations

import io
import os
from datetime import datetime
from typing import Any

import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import TMDB_API_KEY
from Cyra import app
from Cyra.helpers import sc
from Cyra.modules.tmdb import tmdb_get

IMG_BASE = "https://image.tmdb.org/t/p"
SESSIONS: dict[int, dict[str, Any]] = {}

DIMS = {
    "landscape": (1600, 900),
    "hero": (1280, 720),
    "cinema": (1280, 720),
}

PIXEL_PRESETS = [
    "480p | 720p | 1080p",
    "720p | 1080p | 2160p",
    "1080p",
    "480p | 720p",
]

DEFAULTS = {
    "layout": "landscape",
    "caption_tpl": "classic",
    "audio": "Hindi",
    "status": "Completed",
    "pixels": "480p | 720p | 1080p",
    "channel": "DragonByte",
    "cta": "Watch Now",
    "show_overview": True,
}


def _font(size: int, bold: bool = False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _textlen(draw, text, font):
    try:
        return draw.textlength(text, font=font)
    except Exception:
        b = draw.textbbox((0, 0), text, font=font)
        return b[2] - b[0]


def _fit(text, draw, font, max_w):
    if _textlen(draw, text, font) <= max_w:
        return text
    while text and _textlen(draw, text + "...", font) > max_w:
        text = text[:-1]
    return text + "..."


def _wrap(text, draw, font, max_w, max_lines=4):
    words = (text or "").split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if _textlen(draw, test, font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if lines and len(lines) == max_lines:
        lines[-1] = _fit(lines[-1], draw, font, max_w)
    return lines


def _cover(img: Image.Image, w: int, h: int) -> Image.Image:
    ir = img.width / img.height
    tr = w / h
    if ir > tr:
        sh = img.height
        sw = int(img.height * tr)
        sx = (img.width - sw) // 2
        sy = 0
    else:
        sw = img.width
        sh = int(img.width / tr)
        sx = 0
        sy = (img.height - sh) // 2
    crop = img.crop((sx, sy, sx + sw, sy + sh))
    return crop.resize((w, h), Image.Resampling.LANCZOS)


def _gradient_bottom(w, h):
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(h - 1, 1)
        if t < 0.2:
            a = 0
        elif t < 0.45:
            a = int(90 * ((t - 0.2) / 0.25))
        else:
            a = int(90 + 145 * ((t - 0.45) / 0.55))
        d.line([(0, y), (w, y)], fill=(0, 0, 0, min(a, 235)))
    return g


def _gradient_left(w, h):
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    max_x = int(w * 0.55)
    for x in range(max_x):
        a = int(140 * (1 - x / max_x))
        d.line([(x, 0), (x, h)], fill=(0, 0, 0, a))
    return g


def _round_rect(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)


def media_label(d: dict) -> str:
    g = (d.get("genres") or "").lower()
    if "animation" in g or "anime" in g:
        return "ANIME"
    if d.get("type") == "tv":
        return "SERIES"
    return "MOVIE"


async def fetch_bytes(url: str):
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


async def load_details(media_type: str, tmdb_id: int) -> dict | None:
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
    genres = ", ".join(g["name"] for g in (data.get("genres") or [])[:5])
    overview = (data.get("overview") or "")[:500]
    rating = round(float(data.get("vote_average") or 0), 1)
    poster = data.get("poster_path")
    backdrop = data.get("backdrop_path")
    status = data.get("status") or ("Ended" if is_tv else "Released")
    seasons = data.get("number_of_seasons") if is_tv else None
    episodes = data.get("number_of_episodes") if is_tv else None
    logo = None
    logos = (data.get("images") or {}).get("logos") or []
    if logos:
        logos = sorted(
            logos,
            key=lambda x: (0 if x.get("iso_639_1") == "en" else 1, -(x.get("vote_average") or 0)),
        )
        logo = f"{IMG_BASE}/w500{logos[0]['file_path']}"
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
        "logo": logo,
        "status": status,
        "seasons": seasons,
        "episodes": episodes,
        "link": f"https://www.themoviedb.org/{media_type}/{tmdb_id}",
    }


def build_caption(d: dict, s: dict) -> str:
    tpl = s.get("caption_tpl") or "classic"
    title = d["title"]
    year = d.get("year") or ""
    title_line = f"{title} ({year})".strip()
    powered = s.get("channel") or "DragonByte"
    status = s.get("status") or d.get("status") or ""
    pixels = s.get("pixels") or "1080p"
    audio = s.get("audio") or "Hindi"
    rating = d.get("rating")
    episodes = d.get("episodes")
    genres = d.get("genres") or ""
    overview = d.get("overview") or ""

    if tpl == "minimal":
        lines = [title_line]
        if s.get("show_overview") and overview:
            lines.append(overview[:180])
        lines.append(f"Powered by: {powered}")
        return "\n".join(lines)

    if tpl == "compact":
        bits = []
        if status:
            bits.append(status)
        if rating:
            bits.append(f"★ {rating}")
        if pixels:
            bits.append(pixels)
        if audio:
            bits.append(audio)
        lines = [title_line, " · ".join(bits)]
        if genres:
            lines.append(genres)
        lines.append(f"Powered by: {powered}")
        return "\n".join(lines)

    if tpl == "hashtag":
        tags = ["#" + "".join(c for c in title if c.isalnum())]
        for g in genres.split(","):
            t = "".join(c for c in g.strip() if c.isalnum())
            if t:
                tags.append("#" + t)
        tags.append("#PosterFORGE")
        lines = [title_line, " ".join(tags[:8]), f"Powered by: {powered}"]
        return "\n".join(lines)

    # classic (default) — matches website
    lines = [title_line, "╭───────────────────"]
    if status:
        lines.append(f"➥ Status: {status}")
    if episodes:
        lines.append(f"➥ Episodes: {episodes}")
    if rating:
        lines.append(f"➥ Ratings: {rating} TMDb")
    if pixels:
        lines.append(f"➥ Pixels: {pixels}")
    if audio:
        lines.append(f"➥ Audio: {audio}")
    lines.append("├───────────────────")
    if genres:
        lines.append(f"➥ Genres: {genres}")
    lines.append("╰───────────────────")
    if s.get("show_overview") and overview:
        lines.append(f"≡ {overview[:240]}")
    lines.append("╭───────────────────")
    lines.append(f"➥ Powered by: {powered}")
    lines.append("╰───────────────────")
    return "\n".join(lines)


def draw_brand(draw, W, channel: str):
    pad = 36
    y = 36
    name = channel or "DragonByte"
    f_mark = _font(14, True)
    f_name = _font(17, True)
    f_copy = _font(12)
    mark = 28
    name_w = _textlen(draw, name, f_name)
    total = mark + 10 + name_w
    x = W - pad - total
    _round_rect(draw, [x, y - 18, x + mark, y - 18 + mark], 8, (255, 255, 255))
    dw = _textlen(draw, "D", f_mark)
    draw.text((x + (mark - dw) / 2, y - 14), "D", font=f_mark, fill=(10, 10, 10))
    draw.text((x + mark + 10, y - 14), name, font=f_name, fill=(255, 255, 255))
    copy = f"(c) {datetime.now().year}"
    cw = _textlen(draw, copy, f_copy)
    draw.text((W - pad - cw, y + 14), copy, font=f_copy, fill=(180, 180, 180))


def render_poster(d: dict, s: dict, art_bytes, logo_bytes=None) -> bytes:
    layout = s.get("layout") or "landscape"
    W, H = DIMS.get(layout, DIMS["landscape"])
    channel = s.get("channel") or "DragonByte"
    cta = s.get("cta") or "Watch Now"

    if art_bytes:
        try:
            base = Image.open(io.BytesIO(art_bytes)).convert("RGB")
        except Exception:
            base = Image.new("RGB", (W, H), (24, 24, 32))
    else:
        base = Image.new("RGB", (W, H), (24, 24, 32))

    art = _cover(base, W, H)
    if layout == "cinema":
        art = ImageEnhance.Brightness(art).enhance(0.55)
        art = art.filter(ImageFilter.GaussianBlur(2))

    canvas = art.convert("RGBA")
    if layout == "landscape":
        canvas = Image.alpha_composite(canvas, _gradient_left(W, H))
        canvas = Image.alpha_composite(canvas, _gradient_bottom(W, H))
    elif layout == "hero":
        canvas = Image.alpha_composite(canvas, _gradient_bottom(W, H))
        # strong left vignette
        canvas = Image.alpha_composite(canvas, _gradient_left(W, H))
    else:  # cinema
        top = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        td = ImageDraw.Draw(top)
        for y in range(H):
            a = int(160 * abs((y / H) - 0.5) * 2)
            td.line([(0, y), (W, y)], fill=(0, 0, 0, min(a + 40, 200)))
        canvas = Image.alpha_composite(canvas, top)

    draw = ImageDraw.Draw(canvas)
    pad = 64 if layout == "landscape" else 48

    # type badge
    label = media_label(d)
    f_badge = _font(15, True)
    type_w = _textlen(draw, label, f_badge) + 32
    by = 48 if layout != "cinema" else 40
    _round_rect(draw, [pad, by, pad + type_w, by + 34], 8, (255, 255, 255))
    draw.text((pad + 16, by + 8), label, font=f_badge, fill=(10, 10, 10))

    x_meta = pad + type_w + 16
    f_meta = _font(20, True)
    if d.get("year"):
        draw.text((x_meta, by + 6), str(d["year"]), font=f_meta, fill=(220, 220, 220))
        x_meta += _textlen(draw, str(d["year"]), f_meta) + 18
    if d.get("rating"):
        draw.text((x_meta, by + 6), f"* {d['rating']}", font=f_meta, fill=(240, 240, 240))

    # title / logo
    y = 110 if layout == "landscape" else 100
    logo_img = None
    if logo_bytes:
        try:
            logo_img = Image.open(io.BytesIO(logo_bytes)).convert("RGBA")
        except Exception:
            logo_img = None

    max_title_w = int(W * (0.55 if layout == "landscape" else 0.50))
    if logo_img:
        ir = logo_img.width / max(logo_img.height, 1)
        max_h = 110 if layout != "cinema" else 100
        dw = max_title_w
        dh = dw / ir
        if dh > max_h:
            dh = max_h
            dw = dh * ir
        logo_r = logo_img.resize((int(dw), int(dh)), Image.Resampling.LANCZOS)
        canvas.paste(logo_r, (pad, y), logo_r)
        y += int(dh) + 18
    else:
        f_title = _font(52 if layout == "landscape" else 44, True)
        for line in _wrap(d["title"], draw, f_title, max_title_w, 2):
            draw.text((pad, y), line, font=f_title, fill=(255, 255, 255))
            y += f_title.size + 6
        y += 12

    # stats line
    f_stat = _font(18)
    stats = []
    if d.get("seasons"):
        stats.append(f"{d['seasons']} Season" + ("s" if d["seasons"] != 1 else ""))
    if d.get("episodes"):
        stats.append(f"{d['episodes']} Episodes")
    if s.get("status"):
        stats.append(s["status"])
    if s.get("audio"):
        stats.append(s["audio"])
    if s.get("pixels"):
        stats.append(s["pixels"].split("|")[0].strip())
    if stats:
        draw.text((pad, y), "  |  ".join(stats[:5]), font=f_stat, fill=(200, 205, 220))
        y += 28

    # overview
    if s.get("show_overview") and d.get("overview") and layout != "cinema":
        f_ov = _font(17)
        for line in _wrap(d["overview"], draw, f_ov, max_title_w, 3):
            draw.text((pad, y), line, font=f_ov, fill=(180, 188, 205))
            y += f_ov.size + 5

    # CTA button
    f_cta = _font(18, True)
    cta_w = max(190, int(_textlen(draw, cta, f_cta) + 56))
    btn_h = 52
    bx, by2 = pad, H - 48 - btn_h
    _round_rect(draw, [bx, by2, bx + cta_w, by2 + btn_h], 12, (255, 255, 255))
    tw = _textlen(draw, cta, f_cta)
    draw.text((bx + (cta_w - tw) / 2, by2 + 14), cta, font=f_cta, fill=(10, 10, 10))

    # brand corner
    draw_brand(draw, W, channel)

    out = canvas.convert("RGB")
    buf = io.BytesIO()
    out.save(buf, format="JPEG", quality=93)
    buf.seek(0)
    return buf.read()


def studio_keyboard(s: dict) -> InlineKeyboardMarkup:
    layout = s.get("layout", "landscape")
    tpl = s.get("caption_tpl", "classic")
    audio = s.get("audio", "Hindi")
    status = s.get("status", "Completed")
    pixels = s.get("pixels", PIXEL_PRESETS[0])
    ov = s.get("show_overview", True)

    def m(cur, val, label=None):
        lab = label or val
        return ("> " + lab) if cur == val else lab

    # pixel cycle index
    try:
        px_i = PIXEL_PRESETS.index(pixels)
    except ValueError:
        px_i = 0
    next_px = PIXEL_PRESETS[(px_i + 1) % len(PIXEL_PRESETS)]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(sc(m(layout, "landscape", "landscape")), callback_data="pf:set:layout:landscape"),
            InlineKeyboardButton(sc(m(layout, "hero", "hero")), callback_data="pf:set:layout:hero"),
            InlineKeyboardButton(sc(m(layout, "cinema", "cinema")), callback_data="pf:set:layout:cinema"),
        ],
        [
            InlineKeyboardButton(sc(m(tpl, "classic")), callback_data="pf:set:caption_tpl:classic"),
            InlineKeyboardButton(sc(m(tpl, "compact")), callback_data="pf:set:caption_tpl:compact"),
            InlineKeyboardButton(sc(m(tpl, "hashtag")), callback_data="pf:set:caption_tpl:hashtag"),
            InlineKeyboardButton(sc(m(tpl, "minimal")), callback_data="pf:set:caption_tpl:minimal"),
        ],
        [
            InlineKeyboardButton(sc(m(audio, "Hindi")), callback_data="pf:set:audio:Hindi"),
            InlineKeyboardButton(sc(m(audio, "English")), callback_data="pf:set:audio:English"),
            InlineKeyboardButton(sc(m(audio, "Dual")), callback_data="pf:set:audio:Dual"),
        ],
        [
            InlineKeyboardButton(sc(m(status, "Completed")), callback_data="pf:set:status:Completed"),
            InlineKeyboardButton(sc(m(status, "Continuing")), callback_data="pf:set:status:Continuing"),
            InlineKeyboardButton(sc(m(status, "Upcoming")), callback_data="pf:set:status:Upcoming"),
        ],
        [
            InlineKeyboardButton(sc("pixels: ") + pixels.split("|")[0].strip(), callback_data=f"pf:set:pixels:{next_px}"),
            InlineKeyboardButton(sc("overview ") + ("on" if ov else "off"), callback_data="pf:set:overview:toggle"),
        ],
        [
            InlineKeyboardButton(sc("channel"), callback_data="pf:set:channel:ask"),
            InlineKeyboardButton(sc("generate poster"), callback_data="pf:gen"),
            InlineKeyboardButton(sc("caption"), callback_data="pf:cap"),
        ],
        [InlineKeyboardButton(sc("close"), callback_data="pf:close")],
    ])


async def open_studio(cq: CallbackQuery, media_type: str, tmdb_id: int):
    await cq.answer(sc("loading..."))
    d = await load_details(media_type, tmdb_id)
    if not d:
        return await cq.message.edit_text(sc("details not found"))

    uid = cq.from_user.id
    state = {
        **DEFAULTS,
        "data": d,
        "status": d.get("status") or DEFAULTS["status"],
    }
    SESSIONS[uid] = state

    thumb = d.get("backdrop") or d.get("poster")
    cap = (
        f"<b>{d['title']}</b> ({d['year']})\n"
        f"{media_label(d)} · * {d['rating']}\n\n"
        f"<i>{sc('use buttons to change layout / caption / audio')}</i>\n"
        f"<i>{sc('then generate poster')}</i>"
    )
    kb = studio_keyboard(state)
    try:
        await cq.message.delete()
    except Exception:
        pass
    if thumb:
        await app.send_photo(cq.message.chat.id, photo=thumb, caption=cap, reply_markup=kb)
    else:
        await app.send_message(cq.message.chat.id, cap, reply_markup=kb)


@app.on_callback_query(filters.regex(r"^pf:pick:(movie|tv):(\d+)$"))
async def pf_pick(_, cq: CallbackQuery):
    _, _, mt, tid = cq.data.split(":")
    await open_studio(cq, mt, int(tid))


@app.on_callback_query(filters.regex(r"^pf:set:"))
async def pf_set(_, cq: CallbackQuery):
    uid = cq.from_user.id
    state = SESSIONS.get(uid)
    if not state:
        return await cq.answer(sc("session expired — /tmdb again"), show_alert=True)

    parts = cq.data.split(":", 3)
    key, val = parts[2], parts[3]
    if key == "overview":
        state["show_overview"] = not state.get("show_overview", True)
    elif key == "channel":
        await cq.answer()
        return await cq.message.reply_text(
            f"{sc('send new channel name')}\n<code>/setchannel DragonByte</code>"
        )
    else:
        state[key] = val

    SESSIONS[uid] = state
    try:
        await cq.message.edit_reply_markup(reply_markup=studio_keyboard(state))
    except Exception:
        pass
    await cq.answer(sc("updated"))


@app.on_message(filters.command("setchannel"))
async def set_channel(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("<code>/setchannel DragonByte</code>")
    name = " ".join(m.command[1:]).strip()[:32]
    state = SESSIONS.get(m.from_user.id)
    if not state:
        return await m.reply_text(sc("select a title with /tmdb first"))
    state["channel"] = name
    SESSIONS[m.from_user.id] = state
    await m.reply_text(f"{sc('channel set')} → <b>{name}</b>")


@app.on_callback_query(filters.regex(r"^pf:gen$"))
async def pf_gen(_, cq: CallbackQuery):
    uid = cq.from_user.id
    state = SESSIONS.get(uid)
    if not state or "data" not in state:
        return await cq.answer(sc("session expired"), show_alert=True)

    await cq.answer(sc("rendering..."))
    d = state["data"]
    wait = await cq.message.reply_text(sc("rendering poster..."))

    art = await fetch_bytes(d.get("backdrop") or d.get("poster"))
    logo = await fetch_bytes(d.get("logo"))
    try:
        jpg = render_poster(d, state, art, logo)
        caption = build_caption(d, state)
        bio = io.BytesIO(jpg)
        bio.name = "poster.jpg"
        await cq.message.reply_photo(photo=bio, caption=caption[:1024])
        await wait.delete()
    except Exception as e:
        await wait.edit_text(f"<code>{str(e)[:220]}</code>")


@app.on_callback_query(filters.regex(r"^pf:cap$"))
async def pf_cap(_, cq: CallbackQuery):
    state = SESSIONS.get(cq.from_user.id)
    if not state or "data" not in state:
        return await cq.answer(sc("session expired"), show_alert=True)
    await cq.answer()
    await cq.message.reply_text(f"<b>{sc('caption')}</b>\n\n<code>{build_caption(state['data'], state)}</code>")


@app.on_callback_query(filters.regex(r"^pf:close$"))
async def pf_close(_, cq: CallbackQuery):
    SESSIONS.pop(cq.from_user.id, None)
    await cq.answer(sc("closed"))
    try:
        await cq.message.delete()
    except Exception:
        pass


@app.on_message(filters.command(["poster", "posterforge"]))
async def poster_help(_, m: Message):
    await m.reply_text(
        f"<b>{sc('posterforge')}</b>\n\n"
        f"1. <code>/tmdb inception</code>\n"
        f"2. {sc('select a result')}\n"
        f"3. {sc('layout')}: landscape / hero / cinema\n"
        f"4. {sc('caption')}: classic / compact / hashtag / minimal\n"
        f"5. {sc('audio · status · pixels')}\n"
        f"6. <b>{sc('generate poster')}</b>\n\n"
        f"<code>/setchannel YourName</code>\n\n"
        f"<i>{sc('powered by dragonbyte network')}</i>"
    )
