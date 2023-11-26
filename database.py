## database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import SQLALCHEMY_DATABASE_URI

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

# Create an engine bound to the database URL
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

# Create a configured "Session" class
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Create a base class for declarative class definitions
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise
    # you will have to import them first before calling init_db()
    import .models  # Import models to ensure they are known to the Base metadata
    Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    db_session.remove()

# Ensure that the session is properly removed at the end of the request or when the application shuts down
from flask import current_app
current_app.teardown_appcontext(shutdown_session)
