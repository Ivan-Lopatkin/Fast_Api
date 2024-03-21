from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from src.Base import Base


class Seller(Base):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    e_mail: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    books = relationship("Book", back_populates="seller", cascade="all,delete")

metadata = Base.metadata