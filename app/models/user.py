from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)  # nullable for Google users
    phone = Column(String, nullable=True)

    role = Column(Enum(UserRole), default=UserRole.customer)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)