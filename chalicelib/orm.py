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
    birds = relationship('Bird', backref='hunt',
                         cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '<Hunt(id=%s, date=%s, location=%s, timeofday=%s)>'\
            % (self.id, self.date, self.location, self.timeofday)


class Hunter(Base):
    __tablename__ = 'hunter'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(50), nullable=False)

    def __repr__(self):
        return '<Hunter(id=%s, firstname=%s, lastname=%s)>'\
            % (self.id, self.firstname, self.lastname)


class HuntHunter(Base):
    __tablename__ = 'hunt_hunter'
    hunt_id = Column(Integer, ForeignKey('hunt.id'), primary_key=True)
    hunter_id = Column(Integer, ForeignKey('hunter.id'), primary_key=True)
    hunter = relationship('Hunter', backref='hunt_associations')
    hunt = relationship('Hunt', backref='hunter_associations')

    def __repr__(self):
        return '<HuntHunter(hunt_id=%s, hunter_id=%s)>'\
            % (self.hunt_id, self.hunter_id)


class Bird(Base):
    __tablename__ = 'bird'
    id = Column(Integer, primary_key=True)
    species = Column(Enum(*BirdEnum), nullable=False)
    gender = Column(Enum(*BirdGenderEnum), nullable=False)
    banded = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mounted = Column(Boolean, default=False)
    Hunt_id = Column(Integer, ForeignKey('hunt.id'))

    def __repr__(self):
        return '<Bird(id=%s, species=%s, gender=%s,\
                    banded=%s, lost=%s, mounted=%s)>'\
                        % (self.id, self.species, self.gender,
                           self.banded, self.lost, self.mounted)


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
