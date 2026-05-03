import random
import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

USERS_TOTAL = 100

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:6500/postgres"
#DATABASE_URL = "sqlite+aiosqlite:///example.db"
engine = create_async_engine(DATABASE_URL)
sm = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def seed_data() -> None:
    async with sm() as session:
        users = []
        for i in range(USERS_TOTAL):
            first_name = random.choice(['Alex', 'Maria', 'Ivan', 'Sofia', 'Daniel', 
                                'Olivia', 'Maxim', 'Emma', 'Lucas', 'Anna'])
            second_name = random.choice(['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 
                                 'Thomas', 'Jackson', 'White', 'Harris', 'Martin'])
            users.append(User(name=f"{first_name} {second_name}"))
        session.add_all(users)
        await session.commit()


async def main() -> None:
    await init_db()
    await seed_data()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
