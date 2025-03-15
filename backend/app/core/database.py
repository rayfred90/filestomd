from contextlib import contextmanager
from typing import Generator
from sqlmodel import Session, create_engine, SQLModel
from .config import settings

engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def init_db() -> None:
    """Initialize the database, creating all tables."""
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI endpoints that need a database session."""
    with get_session() as session:
        yield session
