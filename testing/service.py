import aiosqlite


async def fetch_user(user_id: int) -> dict:
    async with aiosqlite.connect('users.db') as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(f'SELECT id, name, email FROM users where id={user_id};') as cursor:
            row = await cursor.fetchone()  # row is tuple
    return dict(row)  # {"id": .., "name": .., "email":..}


async def get_user_name(user_id: int) -> str:
    user = await fetch_user(user_id)
    return user["name"]
