# © 2026 DragonByte Network | @flexyy

from pathlib import Path

def list_modules():
    return [
        f.stem for f in Path(__file__).parent.glob("*.py")
        if f.is_file() and f.name != "__init__.py"
    ]

ALL_MODULES = frozenset(sorted(list_modules()))
