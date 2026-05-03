"""
######### for sqlite:
% python buggy_client.py
case async: took time 0.03 sec
case sync: took time 0.06 sec

######### for postgresql with 500ms network latency:
% python buggy_client.py 
case async: took time 11.20 sec
case sync: took time 16.27 sec
"""
import asyncio
from time import time
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select, desc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import select, func, literal


#DATABASE_URL = "postgresql+psycopg://postgres:admin@localhost:6500/postgres"
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
sm = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


#DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:6500/postgres"
DATABASE_URL = "sqlite+aiosqlite:///example.db"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def count_pairs_async(name1: str, name2: str, name3: str, name4: str):
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


async def main_sync():
    await asyncio.gather(
        count_pairs_sync("Daniel", "Emma", "Alex", "Ivan"), 
        count_pairs_sync("Maxim", "Anna", "Sofia", "Lucas"),
        count_pairs_sync("Olivia", "Maria", "Maxim", "Daniel")
    )

async def main_async():
    await asyncio.gather(
        count_pairs_async("Daniel", "Emma", "Alex", "Ivan"), 
        count_pairs_async("Maxim", "Anna", "Sofia", "Lucas"),
        count_pairs_async("Olivia", "Maria", "Maxim", "Daniel")
    )



start_ts = time()
asyncio.run(main_async())
print(f"case async: took time {time() - start_ts:.2f} sec")

start_ts = time()
asyncio.run(main_sync())
print(f"case sync: took time {time() - start_ts:.2f} sec")
