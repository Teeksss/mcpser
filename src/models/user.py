from sqlalchemy import Column, Integer, String, ForeignKey
from src.models.core import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    email = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Integer, default=1)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)