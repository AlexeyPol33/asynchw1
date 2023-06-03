from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import inspect

import asyncio

PG_DNS = 'postgresql+asyncpg://postgres:postgres@localhost:5432/asyncbase'
engine = create_async_engine(PG_DNS)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)

class SwapiPeople(Base):
    __tablename__ = 'swapi_people'

    id = Column(Integer,primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(JSON)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(JSON)
    starships = Column(JSON)
    vehicles = Column(JSON)


async def run_db():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)

async def get_model_keys():

    async with Session() as session:
        model = SwapiPeople  # Ваша модель SwapiPeople

        async with session.begin():
            inspector = inspect(model)
            columns = inspector.columns
            keys = [column.name for column in columns]

        return keys

if __name__ == '__main__':
    asyncio.run(run_db())

