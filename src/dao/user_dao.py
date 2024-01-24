from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDAO
from src.models import User


class UserDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)
