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

''' hunt_hunter_association = Table(
    'HuntDetails', Base.metadata,
    Column('hunt_id', Integer, ForeignKey('Hunts.id')),
    Column('hunter_id', Integer, ForeignKey('Hunters.id'))
) '''


''' class HunterHuntAssociation(Base):
    __tablename__ = 'HunterHuntAssociation'
    hunt_id = Column(Integer, ForeignKey('Hunts.id'), primary_key=True)
    hunter_id = Column(Integer, ForeignKey('Hunters.id'), primary_key=True)
    #hunt = relationship('Hunt', backref="hunts")
    #hunter = relationship('Hunter', backref="hunters")


class Hunt(Base):
    __tablename__ = 'Hunts'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    location = Column(String(50), nullable=False)
    timeofday = Column(Enum(*TimeOfDayEnum), nullable=False)
    birds = relationship('Bird', backref='hunt')
    hunters = relationship('Hunter', backref='hunts')


class Bird(Base):
    __tablename__ = 'Birds'
    id = Column(Integer, primary_key=True)
    hunt_id = Column(Integer, ForeignKey('Hunts.id'), nullable=False)
    species = Column(Enum(*BirdEnum), nullable=False)
    gender = Column(Enum(*BirdGenderEnum), nullable=False)
    banded = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mounted = Column(Boolean, default=False)


class Hunter(Base):
    __tablename__ = 'Hunters'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(50), nullable=False)
    hunts = relationship('HunterHuntAssociation', backref='hunter') '''


''' class Hunt (Base):
    __tablename__ = "Hunt"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    location = Column(String(50), nullable=False)
    timeofday = Column(Enum(*TimeOfDayEnum), nullable=False)


class Hunter (Base):
    __tablename__ = "Hunter"
    id = Column('id', Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(50), nullable=False)


class HuntHunter (Base):
    __tablename__ = "Hunt_Hunter"
    hunt_id = Column(Integer, ForeignKey('Hunt.id'), primary_key=True)
    hunter_id = Column(Integer, ForeignKey('Hunter.id'), primary_key=True)
    hunt = relationship('Hunt', foreign_keys=hunt_id)
    hunter = relationship('Hunter', foreign_keys=hunter_id)


class Bird (Base):
    __tablename__ = "Bird"
    id = Column('id', Integer, primary_key=True)
    species = Column(Enum(*BirdEnum), nullable=False)
    gender = Column(Enum(*BirdGenderEnum), nullable=False)
    banded = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mounted = Column(Boolean, default=False)
    hunt_id = Column('Hunt_id', Integer, ForeignKey('Hunt.id'))
    hunt = relationship('Hunt', foreign_keys=hunt_id) '''


class HuntHunter(Base):
    __tablename__ = 'hunt_hunter'
    hunt_id = Column(Integer, ForeignKey('hunt.id'), primary_key=True)
    hunter_id = Column(Integer, ForeignKey('hunter.id'), primary_key=True)
    hunter = relationship('Hunter', backref='hunt_associations')
    hunt = relationship('Hunt', backref='hunter_associations')


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


class Bird(Base):
    __tablename__ = 'bird'
    id = Column(Integer, primary_key=True)
    species = Column(Enum(*BirdEnum), nullable=False)
    gender = Column(Enum(*BirdGenderEnum), nullable=False)
    banded = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mounted = Column(Boolean, default=False)
    Hunt_id = Column(Integer, ForeignKey('hunt.id'))
