from models import Base


def create_default_tables(engine, session):
    # Create all tables
    Base.metadata.create_all(engine)
