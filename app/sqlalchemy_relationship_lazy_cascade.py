import asyncio
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, select, insert, update, delete, text, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# 创建基类
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    orders = relationship("Order", back_populates="user", lazy='select')
    # orders = relationship("Order", back_populates="user", lazy='joined')
    # orders = relationship("Order", back_populates="user", lazy='subquery')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    created_at = Column(DateTime)
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    # orders = relationship("Order", back_populates="user", cascade="save-update、delete")
