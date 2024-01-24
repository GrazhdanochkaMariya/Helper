# from typing import AsyncGenerator
#
# import pytest
# from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
#
# from src.old.db import (dispose_engine, get_or_create_engine,
#                         get_or_create_session)
# from src.old.db.db import get_db
#
#
# @pytest.mark.asyncio
# async def test_get():
#     """Tests get db"""
#     db = get_db()
#     assert db, "No DB"
#     assert isinstance(db, AsyncGenerator)
#
#
# def test_get_or_create_engine():
#     """Tests get or create engine"""
#     engine = get_or_create_engine()
#     assert engine, "No engine"
#     assert isinstance(engine, AsyncEngine)
#
#
# def test_get_or_create_session():
#     """Tests get or create session"""
#     session = get_or_create_session()
#     assert session, "No session"
#     assert isinstance(session, AsyncSession)
#
#
# @pytest.mark.asyncio
# async def test_dispose_engine():
#     """Tests stop engine"""
#     engine = get_or_create_engine()
#     assert engine
#     from src.old.db import __engine
#
#     assert __engine
#
#     await dispose_engine()
#     from src.old.db import __engine
#
#     assert not __engine
