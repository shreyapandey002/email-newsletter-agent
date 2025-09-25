# models.py
from sqlalchemy import Column, Integer, String, Boolean
from .db import Base

class Subscribers(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    is_subscribed = Column(Boolean, default=True, nullable=False)
