import datetime
from enum import Enum as EnumType

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __str__(self) -> str:
        return f"{self.email}"


class TypeEnum(str, EnumType):
    """Str enum for lead status"""

    CONTACT = "CONTACT"
    DNM = "DNM"
    REQUEST = "REQUEST"
    DECLINED = "DECLINED"


class LeadContact(Base):
    __tablename__ = "lead_contact"

    id = Column(Integer, primary_key=True, nullable=False)
    lead_name = Column(String, nullable=False)
    # where is company ???
    linkedin_profile = Column(String, unique=True, nullable=False, index=True)
    status = Column(ENUM(TypeEnum), default=TypeEnum.CONTACT)
    next_contact = Column(String)

    # support field
    created_at = Column(DateTime, default=datetime.datetime.now)

    def __str__(self) -> str:
        return f"{self.status.name}: {self.linkedin_profile}"
