# © 2026 DragonByte Network | @flexyy

SMALL = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz",
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘզʀꜱᴛᴜᴠᴡxʏᴢ",
)

def sc(text: str) -> str:
    """convert to small caps"""
    return text.translate(SMALL)
