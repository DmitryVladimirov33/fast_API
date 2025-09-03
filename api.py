from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn


from fastapi import FastAPI


app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///users.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session as session:
        yield session


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = MappedColumn(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    age: Mapped[int]


@app.post("/create_database")
async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"success": True}
