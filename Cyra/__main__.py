# © 2026 DragonByte Network | @flexyy

import importlib
from pyrogram import idle
from Cyra import app
from Cyra.modules import ALL_MODULES


async def boot():
    await app.start()
    for mod in ALL_MODULES:
        importlib.import_module(f"Cyra.modules.{mod}")
    await idle()
    await app.stop()


if __name__ == "__main__":
    app.run(boot())
