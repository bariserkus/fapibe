from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:rfjGsU4y9pVyX01@localhost/TodoApplicationDatabase"
#SQLALCHEMY_DATABASE_URL = "postgresql://bariserkus:pass1234@192.168.0.182/testdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base =  declarative_base()