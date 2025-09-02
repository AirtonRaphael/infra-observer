from sqlalchemy.orm import Session

from models import User, PermissionsType, Base
from schema import PermissionEnum
from utils import get_hashed_password


def create_default_tables(engine, session):
    # Create all tables
    Base.metadata.create_all(engine)

    seed_permissions(session)
    seed_root(session)


def seed_permissions(session: Session):
    for perm in PermissionEnum:
        if not session.query(PermissionsType).filter_by(permission_type=perm).first():
            permission = PermissionsType(permission_type=perm)

            session.add(permission)

    session.commit()


def seed_root(session: Session):
    if not session.query(User).first():
        permission = session.query(PermissionsType).filter_by(permission_type=PermissionEnum.admin).first()
        password = get_hashed_password("root")

        new_root = User(username="root", hash_password=password, email="root@root", permission=permission)

        session.add(new_root)
        session.commit()
