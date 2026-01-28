import os
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
# 👇 Mana shu importlar sizda yetishmayotgan edi
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    diaries = relationship("Diary", back_populates="user")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")

class Goal(Base):
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    deadline = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="goals")

class Diary(Base):
    __tablename__ = 'diaries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    sentiment = Column(String(50), nullable=True)
    voice_file_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="diaries")

# 👇 ENG MUHIM QISMI (Buni albatta qo'shing)
# Biz bu yerda to'g'ridan-to'g'ri havolani emas, os.getenv ishlatdik.
engine = create_async_engine(os.getenv('DB_URL'))

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
