from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.session import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    linkedin_profiles = relationship("LinkedInProfile", back_populates="user")


class LinkedInProfile(Base):
    __tablename__ = 'linkedin_profiles'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    linkedin_url = Column(String, unique=True, nullable=False)
    user = relationship("User", back_populates="linkedin_profiles")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
