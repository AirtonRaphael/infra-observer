from sqlalchemy.orm import Session

from models import User, Roles, Base
from schema import RolesEnum
from utils import get_hashed_password


def create_default_tables(engine, session):
    # Create all tables
    Base.metadata.create_all(engine)

    seed_permissions(session)
    seed_root(session)


def seed_permissions(session: Session):
    for role in RolesEnum:
        if not session.query(Roles).filter_by(role=role).first():
            new_role = Roles(role=role)

            session.add(new_role)

    session.commit()


def seed_root(session: Session):
    if not session.query(User).first():
        role = session.query(Roles).filter_by(role=RolesEnum.admin).first()
        password = get_hashed_password("root")

        new_root = User(username="root", hash_password=password, email="root@root", role_id=role.role_id)

        session.add(new_root)
        session.commit()
