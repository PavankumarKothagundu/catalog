import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class BoatCompanyName(Base):
    __tablename__ = 'boatcompanyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="boatcompanyname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class BoatName(Base):
    __tablename__ = 'boatname'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    year = Column(String(150))
    color = Column(String(150))
    capacity = Column(String(150))
    area = Column(String(30))
    volume = Column(String(30))
    motortype = Column(String(250))
    stormpower = Column(String(30))
    date = Column(DateTime, nullable=False)
    boatcompanynameid = Column(Integer, ForeignKey('boatcompanyname.id'))
    boatcompanyname = relationship(
        BoatCompanyName, backref=backref('boatname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="boatname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'year': self. year,
            'color': self. color,
            'capacity': self. capacity,
            'area': self. area,
            'volume': self. volume,
            'motortype': self. motortype,
            'stormpower': self. stormpower,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///boats.db')
Base.metadata.create_all(engin)
