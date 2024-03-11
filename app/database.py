from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_HOST=os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER=os.environ['MYSQL_USER']
MYSQL_PASSWORD=os.environ['MYSQL_PASSWORD']
MYSQL_DB=os.environ['MYSQL_DB']

SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, isolation_level="READ UNCOMMITTED"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()