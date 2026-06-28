from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.config import settings


connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    from backend.models import academic_record, mentor_answer, mentor_report, mentor_session, prediction, recommendation, student  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema()


def ensure_sqlite_schema() -> None:
    if not settings.DATABASE_URL.startswith("sqlite"):
        return
    with engine.begin() as connection:
        existing_columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(recommendations)")).fetchall()
        }
        if "resources_json" not in existing_columns:
            connection.execute(
                text("ALTER TABLE recommendations ADD COLUMN resources_json TEXT NOT NULL DEFAULT '[]'")
            )
