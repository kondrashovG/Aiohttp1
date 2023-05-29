import os

from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.getenv('USERNAME_DB', 'app')
password = os.getenv('PASSWORD_DB', '1234')
host = os.getenv('HOST', '127.0.0.1')
port = os.getenv('PORT', '5431')
db_name = os.getenv('DB_NAME', 'app')


engine = create_async_engine(f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}')
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# engine = create_engine("postgresql://app:1234@127.0.0.1:5431/app")
# Session = sessionmaker(bind=engine)
# Base = declarative_base(bind=engine)


class Ad(Base):
    __tablename__ = "app_ad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    owner = Column(String, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())


# Base.metadata.create_all()
