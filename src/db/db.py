from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_or_create_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Creates async functions"""
    try:
        db = get_or_create_session()
        yield db
    finally:
        await db.close()
