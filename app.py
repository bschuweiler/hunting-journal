from chalice import Chalice, BadRequestError
import json
from sqlalchemy import create_engine, inspect, extract
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from marshmallow import Schema, fields, pprint

from orm import (
    Base, Hunt, Bird, Hunter, HuntHunter,
    HuntSchema, BirdSchema, HunterSchema, HuntHunterSchema
)

_db = 'sqlite:///testdata.db'
_dbEngine = create_engine(_db)
_Session = sessionmaker(bind=_dbEngine)

app = Chalice(app_name='hunting-journal')
app.debug = True


def dbResultsToSchemaObjects(items, schema):
    returnList = []
    for item in items:
        returnList.append(schema.dump(item).data)

    if len(returnList) == 1:
        return returnList[0]
    return returnList


def getAllResources(model, schema):
    session = _Session()
    items = session.query(model).all()
    return dbResultsToSchemaObjects(items, schema)


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

    huntSchema = HuntSchema()
    return dbResultsToSchemaObjects(hunts, huntSchema)


@app.route('/hunts/{id}', methods=['GET'])
def getHunt(id):
    session = _Session()

    hunt = session.query(Hunt).filter(Hunt.id == id)

    huntSchema = HuntSchema()
    return dbResultsToSchemaObjects(hunt, huntSchema)


@app.route('/hunts/{id}/birds', methods=['GET'])
def getBirdsForHunt(id):
    session = _Session()

    birds = session.query(Bird).filter(Bird.Hunt_id == id)
    birdSchema = BirdSchema()
    return dbResultsToSchemaObjects(birds, birdSchema)


@app.route('/hunts', methods=['POST'])
def addHunts():
    session = _Session()

    request = app.current_request
    data = request.json_body
    if not isinstance(data, dict):
        raise BadRequestError(
            'Invalid POST data - endpoint accepts single hunt JSON object')

    # TODO: Make this more specific so you know
    # what's missing or maybe this should be some schema check
    if not data.get('date') or\
       not data.get('location') or\
       not data.get('timeofday') or\
       not data.get('hunters'):
        raise BadRequestError('Missing required information')

    # Get referenced Hunter objects
    hunters = session.query(Hunter).filter(
        Hunter.id.in_(data.get('hunters'))).all()

    # Build up Bird entries
    birds = []
    for bird in data.get('birds'):
        birds.append(Bird(species=bird.get('species'),
                          gender=bird.get('gender'),
                          lost=bird.get('lost'),
                          banded=bird.get('banded'),
                          mounted=bird.get('mounted')))

    # Construct Hunt entries
    hunt = Hunt(date=datetime.strptime(data.get('date'), '%Y-%m-%d'),
                location=data.get('location'),
                timeofday=data.get('timeofday'),
                hunters=hunters,
                birds=birds)

    session.add(hunt)
    session.commit()

    return '{ "id": %d}' % (hunt.id)


# @app.route('/hunts', methods=['DELETE'])
# def deleteHunts():



@app.route('/birds', methods=['GET'])
def getBirds():
    birdSchema = BirdSchema()
    return getAllResources(Bird, birdSchema)


@app.route('/hunters', methods=['GET'])
def getHunters():
    hunterSchema = HunterSchema()
    return getAllResources(Hunter, hunterSchema)
