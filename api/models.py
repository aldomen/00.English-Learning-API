# this file is for the configuration of the database, the tables and the schema for the data.
from database import Base
from sqlalchemy import Column, String, Integer


class EnglishSpanish(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True,index=True)
    english=Column(String)
    spanish=Column(String)
    date=Column(String)
    rep = Column(Integer, default=0)