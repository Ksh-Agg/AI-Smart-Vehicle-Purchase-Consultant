from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """Yield one database session and always close it."""
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
