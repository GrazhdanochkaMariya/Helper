from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.db.db import get_db
from src.db.session import get_or_create_session, get_or_create_engine, dispose_engine


@pytest.mark.asyncio
async def test_get_db():
    """Tests get db"""
    db = get_or_create_session()
    try:
        assert db, "No DB"
        assert isinstance(db, AsyncSession)
    finally:
        await db.close()


@pytest.mark.asyncio
async def test_get():
    """Tests get db"""
    db = get_db()
    assert db, "No DB"
    assert isinstance(db, AsyncGenerator)


def test_get_or_create_engine():
    """Tests get or create engine"""
    engine = get_or_create_engine()
    assert engine, "No engine"
    assert isinstance(engine, AsyncEngine)


def test_get_or_create_session():
    """Tests get or create session"""
    session = get_or_create_session()
    assert session, "No session"
    assert isinstance(session, AsyncSession)


@pytest.mark.asyncio
async def test_dispose_engine():
    """Tests stop engine"""
    engine = get_or_create_engine()
    assert engine
    from src.db.session import __engine

    assert __engine

    await dispose_engine()
    from src.db.session import __engine

    assert not __engine
