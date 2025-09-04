from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Host(Base):
    __tablename__ = 'Hosts'

    idhost: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(unique=True, nullable=False)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)

