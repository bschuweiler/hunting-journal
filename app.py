from chalice import Chalice, BadRequestError
import json
from sqlalchemy import create_engine, inspect, extract
from sqlalchemy.orm import sessionmaker
from datetime import date
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


# @app.route('/hunts', methods=['POST'])
# def addHunt():


@app.route('/birds', methods=['GET'])
def getBirds():
    birdSchema = BirdSchema()
    return getAllResources(Bird, birdSchema)


@app.route('/hunters', methods=['GET'])
def getHunters():
    hunterSchema = HunterSchema()
    return getAllResources(Hunter, hunterSchema)
