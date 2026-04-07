import asyncio


async def fetch_user(user_id: int) -> dict:
    # imagine this calls DB or external API to get user by id
    await asyncio.sleep(0.1)
    return {"id": user_id, "name": "Alice"}


async def get_user_name(user_id: int) -> str:
    user = await fetch_user(user_id)
    return user["name"]