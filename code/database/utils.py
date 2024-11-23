import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database
from code.package_utils import logger
from code.database.declarations.common import Base
from sqlalchemy.orm import sessionmaker

# Database configuration
POSTGRESQL_HOST = "localhost" if os.path.exists(".env") else "postgres.default.svc.cluster.local"
POSTGRESQL_PORT = 5432
POSTGRESQL_USERNAME = "postgres"
POSTGRESQL_PASSWORD = "crazyPass"
DATABASE_NAME = "estate_management"

url = URL.create(
    drivername="postgresql+pg8000",
    username=POSTGRESQL_USERNAME,
    password=POSTGRESQL_PASSWORD,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT,
    database=DATABASE_NAME
)

# Singleton class to create a connection to the database
class SqlEngine(object):
    def __init__(self):
        self.engine = create_engine(url)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            logger.info(f"Database {DATABASE_NAME} created")
        Base.metadata.create_all(self.engine)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SqlEngine, cls).__new__(cls)
            logger.info("Create instance of SqlEngine")
        return cls.instance

    def engine(self):
        return self.engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=SqlEngine().engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


