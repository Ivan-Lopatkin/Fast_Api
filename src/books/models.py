from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from src.Base import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column()
    count_pages: Mapped[int] = mapped_column()
    seller_id: Mapped[int] = mapped_column(ForeignKey("sellers.id"), nullable=False)
    seller = relationship("Seller", back_populates="books")

metadata = Base.metadata
print(metadata)
