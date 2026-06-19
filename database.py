import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Usamos a porta 5435 que configuramos para fugir dos bloqueios do Windows
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://dev_user:dev_password@127.0.0.1:5435/dev_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()