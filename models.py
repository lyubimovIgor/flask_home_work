import os
import atexit
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(PG_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Ad(Base):

    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    title = Column(String(60), index=True, unique=True)
    description = Column(String(120), index=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    author = Column(String(60), index=True, unique=True)


Base.metadata.create_all()
