# © 2026 DragonByte Network | @flexyy

from pyrogram.types import BotCommand

COMMANDS = [
    BotCommand("start", "ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
    BotCommand("help", "ʜᴇʟᴘ & ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ"),
    BotCommand("ping", "ᴄʜᴇᴄᴋ ʟᴀᴛᴇɴᴄʏ"),
    BotCommand("stats", "ʙᴏᴛ ꜱᴛᴀᴛꜱ"),
    BotCommand("id", "ᴜꜱᴇʀ / ᴄʜᴀᴛ ɪᴅ"),
    BotCommand("pinterest", "ᴘɪɴᴛᴇʀᴇꜱᴛ ᴘʜᴏᴛᴏꜱ"),
    BotCommand("tmdb", "ᴍᴏᴠɪᴇ / ꜱᴇʀɪᴇꜱ + ᴘᴏꜱᴛᴇʀ"),
    BotCommand("poster", "ᴘᴏꜱᴛᴇʀꜰᴏʀɢᴇ ꜱᴛᴜᴅɪᴏ"),
    BotCommand("truth", "ᴛʀᴜᴛʜ ǫᴜᴇꜱᴛɪᴏɴ"),
    BotCommand("dare", "ᴅᴀʀᴇ ᴄʜᴀʟʟᴇɴɢᴇ"),
    BotCommand("joke", "ʀᴀɴᴅᴏᴍ ᴊᴏᴋᴇ"),
    BotCommand("quote", "ʀᴀɴᴅᴏᴍ ǫᴜᴏᴛᴇ"),
    BotCommand("ship", "ꜱʜɪᴘ ᴛᴡᴏ ᴜꜱᴇʀꜱ"),
    BotCommand("couple", "ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ"),
    BotCommand("roast", "ꜰᴜɴ ʀᴏᴀꜱᴛ"),
    BotCommand("gayrate", "ɢᴀʏ ʀᴀᴛᴇ ᴍᴇᴛᴇʀ"),
    BotCommand("dice", "ʀᴏʟʟ ᴅɪᴄᴇ"),
    BotCommand("coin", "ꜰʟɪᴘ ᴄᴏɪɴ"),
    BotCommand("choose", "ᴄʜᴏᴏꜱᴇ ᴏᴘᴛɪᴏɴꜱ"),
    BotCommand("info", "ᴜꜱᴇʀ ɪɴꜰᴏ"),
    BotCommand("chatinfo", "ɢʀᴏᴜᴘ ɪɴꜰᴏ"),
    BotCommand("admins", "ʟɪꜱᴛ ᴀᴅᴍɪɴꜱ"),
    BotCommand("warn", "ᴡᴀʀɴ ᴀ ᴜꜱᴇʀ"),
    BotCommand("meme", "ᴛᴇxᴛ ᴍᴇᴍᴇ"),
]


async def setup_bot_menu(app):
    try:
        await app.set_bot_commands(COMMANDS)
    except Exception:
        pass
