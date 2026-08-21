# © 2026 DragonByte Network | @flexyy

from Cyra import db

usersdb = db.users
chatsdb = db.chats


async def add_user(user_id: int, username=None):
    await usersdb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "username": username}},
        upsert=True,
    )


async def add_chat(chat_id: int):
    await chatsdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )


async def get_stats():
    users = await usersdb.count_documents({})
    chats = await chatsdb.count_documents({})
    return users, chats
