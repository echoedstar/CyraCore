# © 2026 DragonByte Network | @flexyy

import importlib
from pyrogram import idle
from Cyra import app
from Cyra.modules import ALL_MODULES
from Cyra.bot_menu import setup_bot_menu


async def boot():
    await app.start()
    await setup_bot_menu(app)
    for mod in ALL_MODULES:
        importlib.import_module(f"Cyra.modules.{mod}")
    await idle()
    await app.stop()


if __name__ == "__main__":
    app.run(boot())
