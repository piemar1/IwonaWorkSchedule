__author__ = 'marcin'


from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Boolean, Unicode, DateTime, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY


Base = declarative_base()
# print(dir(Column))

class DbTeam(Base):
    __tablename__ = 'DbTeam'

    id = Column(Integer, primary_key=True)
    team_name = Column(String(250), nullable=False, unique=True)
    creation_date = Column(String(250))
    crew = Column(String(250), nullable=False)



class DbSchedule(Base):
    __tablename__ = 'DbSchedule'

    id = Column(Integer, primary_key=True)
    schedule_name = Column(String(250), nullable=False, unique=True)
    creation_date = Column(String(250))
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('DbTeam.id'))
    crew = relationship(DbTeam)
    schedule = Column(String(250), nullable=False)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_db.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
