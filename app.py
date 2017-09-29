from chalice import Chalice, BadRequestError
import json
from sqlalchemy import create_engine, inspect, extract
from sqlalchemy.orm import sessionmaker
from datetime import date

from orm import Base, Hunt, Bird, Hunter

_db = 'sqlite:///testdata.db'
_dbEngine = create_engine(_db)
_Session = sessionmaker(bind=_dbEngine)

app = Chalice(app_name='hunting-journal')
app.debug = True

"""
These SQLAlchemy conversion methods to
JSON seem hacky - must be a better way
"""


def alchemyencoder(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def alchemyObjAsDict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def alchemyRowObjsToJson(rows):
    return json.dumps([alchemyObjAsDict(row) for row in rows],
                      default=alchemyencoder)


def getAllResources(model):
    session = _Session()
    items = session.query(model).all()
    return alchemyRowObjsToJson(items)


@app.route('/', methods=['GET'])
def index():
    return {'status': 'up'}


@app.route('/hunts', methods=['GET'])
def getHunts():
    session = _Session()

    queryParams = app.current_request.query_params

    hunts = []
    if not queryParams:
        hunts = session.query(Hunt).all()
    elif queryParams.get('year') is not None:
        hunts = session.query(Hunt).filter(
            extract('year', Hunt.date) == queryParams.get('year'))
    else:
        raise BadRequestError('unknown query parameter on request')

    return alchemyRowObjsToJson(hunts)


@app.route('/hunts/{id}', methods=['GET'])
def getHunt(id):
    session = _Session()

    hunt = session.query(Hunt).filter(Hunt.id == id)
    return alchemyRowObjsToJson(hunt)


@app.route('/hunts/{id}/birds', methods=['GET'])
def getBirdsForHunt(id):
    session = _Session()

    birds = session.query(Bird).filter(Bird.Hunt_id == id)
    return alchemyRowObjsToJson(birds)


# @app.route('/hunts', methods=['POST'])
# def addHunt():


@app.route('/birds', methods=['GET'])
def getBirds():
    return getAllResources(Bird)


@app.route('/hunters', methods=['GET'])
def getHunters():
    return getAllResources(Hunter)
