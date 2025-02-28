from sqlalchemy import BigInteger, String, CHAR, select, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, db
from db.utils import CreatedModel


class User(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(56), nullable=True)
    lang: Mapped[str] = mapped_column(CHAR(3), server_default="uz")

    @classmethod
    async def get_ids(cls):
        query = select(cls.id)
        results = await db.execute(query)
        ids = [row[0] for row in results]
        return ids

    @classmethod
    async def exists_user(cls, id_):
        query = select(cls.id).where(cls.id == id_)
        result = await db.execute(query)
        return not bool(result.first())


class Admin(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)


class Group(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    force: Mapped[bool] = mapped_column(Boolean, default=True)

    @classmethod
    async def exists_group(cls, id_):
        query = select(cls.id).where(cls.id == id_)
        result = await db.execute(query)
        return result.scalar() is not None

    @classmethod
    async def get_group_ids(cls) -> list[int]:
        query = select(cls.id)
        results = await db.execute(query)
        ids = [row[0] for row in results.fetchall()]
        return ids


metadata = Base.metadata
