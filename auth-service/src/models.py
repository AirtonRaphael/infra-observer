from sqlalchemy import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship, declarative_base

from schema import PermissionEnum

Base = declarative_base()


class PermissionsType(Base):
    __tablename__ = "PermissionType"

    permission_id: Mapped[int] = mapped_column(primary_key=True)
    permission_type: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum), unique=True, nullable=False)


class User(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey(PermissionsType.permission_id))

    permission: Mapped[PermissionsType] = relationship(PermissionsType, lazy="joined")
