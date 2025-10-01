from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:bunny123@localhost:3306/hostel_form')
SQLALCHEMY_DATABASE_URL2 = os.getenv('DATABASE_URL', 'mysql+pymysql://root:bunny123@localhost:3306/tenant')
SQLALCHEMY_DATABASE_URL3 = os.getenv('DATABASE_URL', 'mysql+pymysql://root:bunny123@localhost:3306/login_form')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine2 = create_engine(SQLALCHEMY_DATABASE_URL2)
engine3 = create_engine(SQLALCHEMY_DATABASE_URL3)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)
SessionLocal3 = sessionmaker(autocommit=False, autoflush=False, bind=engine3)
Base = declarative_base()
Base2 = declarative_base()
Base3 = declarative_base()

