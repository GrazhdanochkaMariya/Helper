"""Module contains functions to create db connection"""
import os
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

try:
    DB_PORT = int(DB_PORT)
except (ValueError, TypeError):
    raise ValueError(f"DB_PORT must be a valid integer.DB_PORT: {DB_PORT}, DB_USER: {DB_USER}, DB_PASS: {DB_PASS}, DB_HOST: {DB_HOST}, DB_NAME: {DB_NAME}")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()

metadata = MetaData()

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session