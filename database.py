from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine('postgresql://postgres:5555@localhost/instagram_new', echo=True)
Base = declarative_base()
Session = sessionmaker()
