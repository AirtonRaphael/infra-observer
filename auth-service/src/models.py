from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from config.database import Base


class PermissionsType(Base):
    __tablename__ = "PermissionType"

    permission_id: Mapped[int] = mapped_column(primary_key=True)
    permission_type: Mapped[str] = mapped_column(unique=True)


class User(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("PermissionType.permission_id"))
    permission: Mapped["PermissionsType"] = relationship()

    @property
    def permission_str(self) -> str:
        return self.permission.permission_type if self.permission else ""
