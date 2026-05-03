"""run server with: 
uvicorn buggy_server:app --reload --host 127.0.0.1 --port 8000 --workers 1 
"""
# select * from users where name like 'Daniel%' order by name;
# select * from users where id=15;

import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select, desc
from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import select, func, literal

DATABASE_URL = "postgresql+psycopg://postgres:admin@localhost:6500/postgres"
#DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
sm = sessionmaker(bind=engine)


app = FastAPI()

@app.on_event("startup")
async def enable_slow_tasks_logging():
    loop = asyncio.get_running_loop()
    loop.set_debug(True)  # enable debug mode for event loop
    loop.slow_callback_duration = 0.02  # duration in sec to be 'slow'

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:6500/postgres"
#DATABASE_URL = "sqlite+aiosqlite:///example.db"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@app.get("/users/{firstname}")
async def get_user_by_firstname(firstname: str):
    async with SessionLocal() as session:
        result = await session.scalars(
            select(User).where(User.name.like(f"{firstname}%")).order_by(desc(User.name))
        )
        users = result.all()
    return [{"name": user.name} for user in users]


@app.get("/users_sync/{firstname}")
def get_user_by_firstname_sync(firstname: str):
    with sm() as session:
        result = session.scalars(
            select(User).where(User.name.like(f"{firstname}%")).order_by(desc(User.name))
        )
        users = result.all()
    return [{"name": user.name} for user in users]


@app.get("/count_pairs/")
async def count_pairs(name1: str, name2: str, name3: str, name4: str):
    u1 = aliased(User)
    u2 = aliased(User)
    u3 = aliased(User)
    u4 = aliased(User)
    count = 0
    async with SessionLocal() as session:
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name1}%"),
                u2.name.like(f"{name2}%"),
                u3.name.like(f"{name3}%"),
                u4.name.like(f"{name4}%"),
            )
        )
        result = await session.scalars(stmt)
        count = +result.one()
        # ----
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name2}%"),
                u2.name.like(f"{name3}%"),
                u3.name.like(f"{name4}%"),
                u4.name.like(f"{name1}%"),
            )
        )
        result = await session.scalars(stmt)
        count = +result.one()
        # ----
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name3}%"),
                u2.name.like(f"{name4}%"),
                u3.name.like(f"{name1}%"),
                u4.name.like(f"{name2}%"),
            )
        )
        result = await session.scalars(stmt)
        count += result.one()
        # ----
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name4}%"),
                u2.name.like(f"{name1}%"),
                u3.name.like(f"{name2}%"),
                u4.name.like(f"{name3}%"),
            )
        )
        result = await session.scalars(stmt)
        count = +result.one()
    return {"pairs": count} 


@app.get("/count_pairs_sync/")
async def count_pairs_sync(name1: str, name2: str, name3: str, name4: str):
    # !!!!!!! fastapi runs sync function in separate thread (threadpool)
    #         so it will be more performant than async version !!!!!!!
    u1 = aliased(User)
    u2 = aliased(User)
    u3 = aliased(User)
    u4 = aliased(User)
    count = 0
    with sm() as session:
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name1}%"),
                u2.name.like(f"{name2}%"),
                u3.name.like(f"{name3}%"),
                u4.name.like(f"{name4}%"),
            )
        )
        result = session.scalars(stmt)
        count += result.one()
        # ----
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name2}%"),
                u2.name.like(f"{name3}%"),
                u3.name.like(f"{name4}%"),
                u4.name.like(f"{name1}%"),
            )
        )
        result = session.scalars(stmt)
        count += result.one()
        # ----
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name3}%"),
                u2.name.like(f"{name4}%"),
                u3.name.like(f"{name1}%"),
                u4.name.like(f"{name2}%"),
            )
        )
        result = session.scalars(stmt)
        count += result.one()
        # ----
        stmt = (
            select(func.count())
            .select_from(u1)
            .join(u2, literal(True))  # CROSS JOIN
            .join(u3, literal(True))  # CROSS JOIN
            .join(u4, literal(True))  # CROSS JOIN
            .where(
                u1.name.like(f"{name4}%"),
                u2.name.like(f"{name1}%"),
                u3.name.like(f"{name2}%"),
                u4.name.like(f"{name3}%"),
            )
        )
        result = session.scalars(stmt)
        count += result.one()
    return {"pairs": count} 


@app.get("/ping")
async def ping():
    return {"ok": True}


@app.get("/user/{id_}")
async def get_user_by_id(id_: int):
    #import pdb; pdb.set_trace()
    async with SessionLocal() as session:
        result = await session.scalars(
            select(User).where(User.id == id_)
        )
        user = result.one()
    return {"name": user.name}


@app.get("/user_sync/{id_}")
async def get_user_by_id_sync(id_: int):
    #import pdb; pdb.set_trace()
    with sm() as session:
        result = session.scalars(
            select(User).where(User.id == id_)
        )
        user = result.one()
    return {"name": user.name}