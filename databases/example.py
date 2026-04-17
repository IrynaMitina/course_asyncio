import asyncio
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


# --------------------
# Base model
# --------------------
class Base(DeclarativeBase):
    pass


# --------------------
# Movie model
# --------------------
class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    director: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int]


# --------------------
# DB setup
# --------------------
#DATABASE_URL = "sqlite+aiosqlite:///movies.db"  # sqlite 
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:6500/movies_db"  # postgresql
#DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/movies_db"  # mysql

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# --------------------
# Create tables
# --------------------
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# --------------------
# Seed demo data
# --------------------
async def seed_data() -> None:
    async with SessionLocal() as session:
        result = await session.execute(select(Movie))
        existing_movies = result.scalars().all()
        if existing_movies:
            return

        session.add_all(
            [
                Movie(title="Inception", director="Christopher Nolan", year=2010),
                Movie(title="The Matrix", director="The Wachowskis", year=1999),
                Movie(title="Interstellar", director="Christopher Nolan", year=2014),
            ]
        )
        await session.commit()


# --------------------
# Fetch all movies
# --------------------
async def get_all_movies() -> list[Movie]:
    async with SessionLocal() as session:
        result = await session.execute(select(Movie))
        movies = result.scalars().all()
        return movies


# --------------------
# Main
# --------------------
async def main() -> None:
    await init_db()
    await seed_data()

    movies = await get_all_movies()

    for movie in movies:
        print(movie.id, movie.title, movie.director, movie.year)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())








engine = create_async_engine(DATABASE_URL, echo=True,)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_data() -> None:
    async with SessionLocal() as session:
        result = await session.execute(select(Movie))
        existing_movies = result.scalars().all()
        if existing_movies:
            return

        session.add_all(
            [
                Movie(title="Inception", director="Christopher Nolan", year=2010),
                Movie(title="The Matrix", director="The Wachowskis", year=1999),
                Movie(title="Interstellar", director="Christopher Nolan", year=2014),
            ]
        )
        await session.commit()


async def get_all_movies() -> list[Movie]:
    async with SessionLocal() as session:
        result = await session.execute(select(Movie))
        return result.scalars().all()


async def main() -> None:
    await init_db()
    await seed_data()

    movies = await get_all_movies()
    for movie in movies:
        print(movie.id, movie.title, movie.director, movie.year)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())





