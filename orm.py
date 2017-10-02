from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    Boolean,
    Date,
    Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import ModelSchema


Base = declarative_base()


TimeOfDayEnum = (
    'Morning',
    'Afternoon',
)

BirdEnum = (
    'American Wigeon',
    'Blue-winged Teal',
    'Bufflehead',
    'Canada',
    'Canvasback',
    'Common Goldeneye',
    'Gadwall',
    'Green-winged Teal',
    'Greater Scaup',
    'Hooded Merganser',
    'Lesser Scaup',
    'Redhead',
    'Ring-necked Duck',
    'Mallard',
    'Northern Pintail',
    'Northern Shoveler',
    'Wood Duck'
)

BirdGenderEnum = (
    'Drake',
    'Hen',
    'Unknown'
)


class Hunt(Base):
    __tablename__ = 'hunt'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    location = Column(String(50), nullable=False)
    timeofday = Column(Enum(*TimeOfDayEnum), nullable=False)
    hunters = relationship('Hunter', secondary='hunt_hunter')
    birds = relationship('Bird', backref='hunt')


class Hunter(Base):
    __tablename__ = 'hunter'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(50), nullable=False)


class HuntHunter(Base):
    __tablename__ = 'hunt_hunter'
    hunt_id = Column(Integer, ForeignKey('hunt.id'), primary_key=True)
    hunter_id = Column(Integer, ForeignKey('hunter.id'), primary_key=True)
    hunter = relationship('Hunter', backref='hunt_associations')
    hunt = relationship('Hunt', backref='hunter_associations')


class Bird(Base):
    __tablename__ = 'bird'
    id = Column(Integer, primary_key=True)
    species = Column(Enum(*BirdEnum), nullable=False)
    gender = Column(Enum(*BirdGenderEnum), nullable=False)
    banded = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mounted = Column(Boolean, default=False)
    Hunt_id = Column(Integer, ForeignKey('hunt.id'))


class HuntSchema(ModelSchema):
    class Meta:
        model = Hunt


class HunterSchema(ModelSchema):
    class Meta:
        model = Hunter


class HuntHunterSchema(ModelSchema):
    class Meta:
        model = HuntHunter


class BirdSchema(ModelSchema):
    class Meta:
        model = Bird
