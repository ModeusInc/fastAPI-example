import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# POSTGRESQL_DB_URL = (
#    f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
#    f"@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}")

POSTGRESQL_DB_URL = settings.DATABASE_URL

print(POSTGRESQL_DB_URL)
engine = create_engine(POSTGRESQL_DB_URL)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password='Sanchez7', cursor_factory=RealDictCursor)
        # Live session with the database
        cursor = conn.cursor()
        print("Database connected successfuly!")
        break
    except Exception as error:
        print("connection failed The error was ", error)
        time.sleep(3)
