from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


############################################# model
class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    director: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int]


############################################# db setup
DATABASE_URL = "sqlite:///movies.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


############################################# create table, insert data
def init_db() -> None:
    Base.metadata.create_all(engine)


def seed_data() -> None:
    with SessionLocal() as session:
        existing_movies = session.execute(select(Movie)).scalars().all()
        if existing_movies:
            return
        session.add_all(
            [
                Movie(title="Inception", director="Christopher Nolan", year=2010),
                Movie(title="The Matrix", director="The Wachowskis", year=1999),
                Movie(title="Interstellar", director="Christopher Nolan", year=2014),
            ]
        )
        session.commit()


############################################# query all movies
def get_all_movies() -> list[Movie]:
    with SessionLocal() as session:
        result = session.execute(select(Movie))
        return result.scalars().all()


############################################# main
def main() -> None:
    init_db()
    seed_data()
    movies = get_all_movies()
    for movie in movies:
        print(movie.id, movie.title, movie.director, movie.year)


if __name__ == "__main__":
    main()
