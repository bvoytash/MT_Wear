from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the database engine
engine = create_async_engine(settings.DB_URL, echo=True, future=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session
