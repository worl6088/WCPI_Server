from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
import logging

engine = create_engine('sqlite:///camera.db', echo=True)
Base = declarative_base()
Base.metadata.drop_all(engine)


class Cam_1(Base):
   __tablename__ = 'cam1_result'
   id =  Column(Integer, primary_key = True)
   start_time = Column(String, nullable=False)
   end_time = Column(String, nullable=False)
   person_image = Column(String(100), nullable=False)


class Cam_2(Base):
   __tablename__ = 'cam2_result'
   id =  Column(Integer, primary_key = True)
   start_time = Column(String, nullable=False)
   end_time = Column(String, nullable=False)
   person_image = Column(String(100), nullable=False)

class Cam_3(Base):
   __tablename__ = 'cam3_result'
   id =  Column(Integer, primary_key = True)
   start_time = Column(String, nullable=False)
   end_time = Column(String, nullable=False)
   person_image = Column(String(100), nullable=False)


def initialize_db():
   Base.metadata.create_all(engine)



initialize_db()