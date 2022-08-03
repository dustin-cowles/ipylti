from os import environ
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_TYPE = environ.get("DB_TYPE", "sqlite")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_NAME = environ.get("DB_NAME", "development")
DB_USER = urllib.parse.quote_plus(environ.get("DB_USER"))
DB_PASSWORD = urllib.parse.quote_plus(environ.get("DB_PASSWORD"))

connect_url = URL(
  environ.get("DB_TYPE", "sqlite"),
  environ.get("DB_USER"),
  environ.get("DB_PASSWORD"),
  environ.get("DB_HOST"),
  environ.get("DB_PORT"),
  environ.get("DB_NAME", "development"),
  {"check_same_thread": false} if DB_TYPE == "sqlite" else {}
)

engine = create_engine(connect_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
