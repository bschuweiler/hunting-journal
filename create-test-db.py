from orm import Base, Hunt, Bird, Hunter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

_db = 'sqlite:///testdata.db'


def insertSampleData(session):
    bill = Hunter(firstname='Bill', lastname='Berditzman')
    johnd = Hunter(firstname='John', lastname='Doe')
    frank = Hunter(firstname='Frank', lastname='Anyman')
    annie = Hunter(firstname='Annie', lastname='Oakley')
    jane = Hunter(firstname='Jane', lastname='Doe')
    johns = Hunter(firstname='John', lastname='Smith')

    hunts = [
        Hunt(date=date(2014, 9, 27),
             location='Cool Island',
             timeofday='Morning',
             birds=[
                Bird(species='Wood Duck', gender='Drake'),
                Bird(species='Canada', gender='Unknown'),
                Bird(species='Canada', gender='Unknown'),
                Bird(species='Wood Duck', gender='Hen'),
                Bird(species='Common Goldeneye', gender='Hen')
             ],
             hunters=[bill, johnd]
             ),
        Hunt(date=date(2014, 9, 27),
             location='Grassy Slough',
             timeofday='Afternoon',
             hunters=[bill, johnd]),
        Hunt(date=date(2015, 10, 9),
             location='Rice Shoreline',
             timeofday='Morning',
             birds=[
                Bird(species='Lesser Scaup', gender='Drake'),
                Bird(species='Lesser Scaup', gender='Drake'),
                Bird(species='Lesser Scaup', gender='Hen'),
                Bird(species='Redhead', gender='Hen'),
                Bird(species='Redhead', gender='Hen')
             ],
             hunters=[bill, annie]
             ),
        Hunt(date=date(2015, 10, 17),
             location='Marshy Point',
             timeofday='Morning',
             birds=[
                Bird(species='Ring-necked Duck', gender='Drake'),
                Bird(species='Ring-necked Duck', gender='Drake'),
                Bird(species='Ring-necked Duck', gender='Hen'),
                Bird(species='Lesser Scaup', gender='Drake'),
                Bird(species='Lesser Scaup', gender='Drake'),
                Bird(species='Common Goldeneye', gender='Drake'),
                Bird(species='Hooded Merganser', gender='Hen')
             ],
             hunters=[bill, johnd, frank, annie, johns, jane]
             ),
        Hunt(date=date(2016, 9, 29),
             location='Cool Island',
             timeofday='Morning',
             birds=[
                Bird(species='Wood Duck', gender='Drake'),
                Bird(species='Wood Duck', gender='Hen'),
                Bird(species='Wood Duck', gender='Drake'),
                Bird(species='Wood Duck', gender='Hen')
             ],
             hunters=[frank, jane]
             ),
        Hunt(date=date(2016, 10, 13),
             location='Marshy Point',
             timeofday='Morning',
             birds=[
                Bird(species='Ring-necked Duck', gender='Hen'),
                Bird(species='Ring-necked Duck', gender='Hen'),
                Bird(species='Ring-necked Duck', gender='Drake'),
                Bird(species='Northern Pintail', gender='Hen')
             ],
             hunters=[annie, johnd, johns]
             )
    ]

    session.add_all(hunts)
    session.commit()


if __name__ == '__main__':
    engine = create_engine(_db)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    insertSampleData(session)
