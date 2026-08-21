# © 2026 DragonByte Network | @flexyy

# small caps map — q has no dedicated small-cap glyph, keep normal q
_SMALL = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ", "g": "ɢ",
    "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ",
    "o": "ᴏ", "p": "ᴘ", "q": "q", "r": "ʀ", "s": "ꜱ", "t": "ᴛ", "u": "ᴜ",
    "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ",
}


def sc(text: str) -> str:
    out = []
    for ch in text:
        low = ch.lower()
        if low in _SMALL:
            out.append(_SMALL[low])
        else:
            out.append(ch)
    return "".join(out)
