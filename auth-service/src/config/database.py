from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config.settings import DB_URL

SessionLocal = None

Base = declarative_base()


def start_db() -> None:
    global SessionLocal

    engine = create_engine(DB_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(engine)


def get_session() -> Session:
    with SessionLocal() as session:
        yield session


def get_closed_session() -> Session:
    return SessionLocal
