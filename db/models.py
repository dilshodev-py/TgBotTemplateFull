import asyncio

from sqlalchemy import String, DECIMAL, select, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from db import Base, db
from db.utils import CreatedModel

class Category(CreatedModel):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(255))
    products : Mapped[list['Product']] = relationship(back_populates="category")
    def __str__(self):
        return self.name
# ctrl + space*2
class Product(CreatedModel):
    name : Mapped[str] = mapped_column(String(55), nullable=True)
    price : Mapped[float] = mapped_column(DECIMAL(9,2))
    category_id : Mapped[int] = mapped_column(ForeignKey("categories.id" , ondelete="CASCADE"), nullable=True)
    category: Mapped['Category'] = relationship(back_populates="products")
    @classmethod
    async def get_by_name(cls, name):
        query = select(cls).where(cls.name.ilike(f"%{name}%"))
        objects = await db.execute(query)
        object_ = objects.scalars()
        if object_:
            return object_
        else:
            return []

metadata = Base.metadata

