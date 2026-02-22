from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Dependency for SQLite database
# The check_same_thread=False is needed for SQLite to work with FastAPI
SQLALCHEMY_DATABASE_URL = "sqlite:///./todolist.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency func to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
