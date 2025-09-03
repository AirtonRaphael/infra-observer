from sqlalchemy import Enum, ForeignKey, select
from sqlalchemy.orm import mapped_column, Mapped, declarative_base, column_property

from schema import RolesEnum

Base = declarative_base()


class Roles(Base):
    __tablename__ = "Roles"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[RolesEnum] = mapped_column(Enum(RolesEnum), unique=True, nullable=False)


class User(Base):
    __tablename__ = "Users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey(Roles.role_id))

    role: Mapped[str] = column_property(
        select(Roles.role)
        .where(Roles.role_id == role_id)
        .scalar_subquery()
    )
