
# 3. Making a database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# this creates a new database. connect_args allows us to pass arguements to the 
# connect_args={"check_same_thread":False} is passing an argument to SQLite,
# instructing it not to check if the connection is being made from the same thread as
# the one that created it. This is particularly useful in scenarios where SQLite is
# used in a single-threaded environment like Flask development servers.
# When check_same_thread is set to False, it disables SQLite's built-in check
# which would raise an exception if an attempt is made to use the connection from a different thread than the one it was created in. This can be necessary for certain applications, but it's important to be cautious when disabling this check, as it can lead to issues in multi-threaded environment
# 
engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args={"check_same_thread":False})
# autocommit = False means sql alchemy qont make changes automatically to the database.
# bind = engine specified database engine
SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind = engine)


# Declarative base allows us to define the database models as Python classes.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()