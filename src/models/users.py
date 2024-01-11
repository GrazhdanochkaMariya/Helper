import datetime
from enum import Enum as EnumType


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM

from src.db.session import Base


class TypeEnum(str, EnumType):
    """Str enum for lead status"""

    CONTACT = "CONTACT"
    DNM = "DNM"


class Contact(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    lead_name = Column(String, nullable=False)
    lead_company = Column(String, nullable=True)
    linkedin_profile = Column(String, unique=True, nullable=False, index=True)
    contact = Column(String, nullable=False)
    status = Column(ENUM(TypeEnum), default=TypeEnum.CONTACT)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    last_login = Column(DateTime, default=datetime.datetime.now)

