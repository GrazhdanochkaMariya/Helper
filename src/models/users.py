import datetime
from enum import Enum as EnumType


from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM

from src.db.session import Base


class TypeEnum(str, EnumType):
    """Str enum for lead status"""

    CONTACT = "CONTACT"
    DNM = "DNM"
    REQUEST = "REQUEST"
    DECLINED = "DECLINED"


class Contact(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    lead_name = Column(String, nullable=False)
    linkedin_profile = Column(String, unique=True, nullable=False, index=True)
    status = Column(ENUM(TypeEnum), default=TypeEnum.CONTACT)
    created_at = Column(DateTime, default=datetime.datetime.now)
    next_contact = Column(DateTime)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    last_login = Column(DateTime, default=datetime.datetime.now)

