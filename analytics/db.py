from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:postgres@db:5432/expense"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
