from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    description = Column(String, nullable=True)


# SQLite connection
engine = create_engine(r"sqlite:///\\shared\WindowsDrive\path\to\database.sqlite")
SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    return SessionLocal()
