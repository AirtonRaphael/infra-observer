from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.settings import DB_URL
from config.setup_db import create_default_tables

SESSION = None


def start_db() -> None:
    global SESSION

    engine = create_engine(DB_URL)

    SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SESSION() as session:
        create_default_tables(engine, session)


def get_session() -> Session:
    with SESSION() as session:
        yield session


def get_closed_session() -> Session:
    return SESSION
