from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from src.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(512))
    role = Column(Enum(UserRole), default=UserRole.user)
    # psu = relationship("Psu", back_populates="user")
