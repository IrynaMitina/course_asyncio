import asyncio
from typing import List

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


############################################# models
class Base(AsyncAttrs, DeclarativeBase):  # mixin AsyncAttrs - to lazy-load attributes
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="posts")


############################################# db setup
DATABASE_URL = "sqlite+aiosqlite:///example.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # to print sql executed (to see when lazy loading is triggered)
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


############################################# create table, insert data
async def init_db() -> None:
    # special DLL functions such as MetaData.create_all() don't include an awaitable hook
    # so we call AsyncConnection.run_sync()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def seed_data() -> None:
    async with SessionLocal() as session:
        alice = User(name="Alice")
        bob = User(name="Bob")

        session.add_all(
            [
                alice,
                bob,
                Post(title="Alice post 1", user=alice),
                Post(title="Alice post 2", user=alice),
                Post(title="Bob post 1", user=bob),
            ]
        )
        await session.commit()


############################################# demo lazy loading attributes via AsyncAttrs
async def demo_asyncattrs() -> None:
    async with SessionLocal() as session:
        print("****************************************************************************** loading user")
        result = await session.execute(
            select(User).where(User.name == "Alice")
        )
        user = result.scalar_one()
        print(f"User loaded: {user.name}")

        # !!! posts relationship is lazy-loaded explicitly through awaitable_attrs
        print("****************************************************************************** loading posts")
        posts = await user.awaitable_attrs.posts
        print("Posts:")
        for post in posts:
            print(f"- {post.title}")


############################################# main
async def main() -> None:
    await init_db()
    await seed_data()
    await demo_asyncattrs()
    await engine.dispose()  # close & clean-up pooled connections


if __name__ == "__main__":
    asyncio.run(main())
