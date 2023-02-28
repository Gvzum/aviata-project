from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession, async_sessionmaker

from config.settings import settings


engine = create_engine(settings.database_url)
SessionSync = scoped_session(
    sessionmaker(autoflush=False, autocommit=False, bind=engine, expire_on_commit=False),
)

async_engine = create_async_engine(settings.async_database_url)
SessionAsync = async_scoped_session(
    async_sessionmaker(bind=async_engine, class_=AsyncSession, autoflush=False, autocommit=False, expire_on_commit=False),
    scopefunc=current_task
)
