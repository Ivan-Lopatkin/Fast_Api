from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from database import Base, engine


class Users(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True, unique=True)
    e_mail: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)


metadata = Base.metadata
metadata.create_all(engine)