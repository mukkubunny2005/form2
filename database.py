import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------------
# Helper function
# ----------------------------
def get_database_url(env_var, default_url):
    return os.getenv(env_var, default_url)

# ----------------------------
# DB URLs
# ----------------------------
SQLALCHEMY_DATABASE_URL = get_database_url(
    "DATABASE_URL",  # Render env variable
    "mysql+pymysql://root:bunny123@localhost:3306/hostel_form"  # Local fallback
)

SQLALCHEMY_DATABASE_URL2 = get_database_url(
    "DATABASE_URL2",
    "mysql+pymysql://root:bunny123@localhost:3306/tenant"
)

SQLALCHEMY_DATABASE_URL3 = get_database_url(
    "DATABASE_URL3",
    "mysql+pymysql://root:bunny123@localhost:3306/login_form"
)

# ----------------------------
# Engines
# ----------------------------
engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine2 = create_engine(SQLALCHEMY_DATABASE_URL2)
engine3 = create_engine(SQLALCHEMY_DATABASE_URL3)

# ----------------------------
# Sessions
# ----------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)
SessionLocal3 = sessionmaker(autocommit=False, autoflush=False, bind=engine3)

# ----------------------------
# Base Models
# ----------------------------
Base = declarative_base()
Base2 = declarative_base()
Base3 = declarative_base()
