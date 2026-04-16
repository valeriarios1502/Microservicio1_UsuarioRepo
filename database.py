from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL",  "postgresql+psycopg2://user:password@3.87.243.107:5432/usuarios_db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"connect_timeout": 5}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
