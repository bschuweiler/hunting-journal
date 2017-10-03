from chalice import Chalice, BadRequestError, NotFoundError, Response
import collections
from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from orm import (
    Base, Hunt, Bird, Hunter, HuntHunter,
    HuntSchema, BirdSchema, HunterSchema, HuntHunterSchema
)

_db = 'sqlite:///testdata.db'
_dbEngine = create_engine(_db)
_Session = sessionmaker(bind=_dbEngine)

app = Chalice(app_name='hunting-journal')
app.debug = True

# TODO: Tests
# TODO: Update endpoints for hunt (PUT)
# TODO: Authentication? (or just defer to hosting w/AWS and API Gateway front?)
# TODO: HTTP caching ETag or Last-Modified w/ 304, etc. when appropriate


def dbResultsToSchemaObjects(results, schema):
    if isinstance(results, collections.Iterable):
        returnList = []
        for result in results:
            returnList.append(schema.dump(result).data)

        if len(returnList) == 1:
            return returnList[0]
        return returnList
    else:
        return schema.dump(results).data


def getAllResources(model, schema):
    session = _Session()
    items = session.query(model).all()
    return dbResultsToSchemaObjects(items, schema)


def validateHuntRequestBody(json):
    if not isinstance(json, dict):
        raise BadRequestError(
            'Invalid POST data - endpoint accepts single hunt JSON object')

    # TODO: Make this more specific so you know
    # what's missing or maybe this should be some schema check
    # and include field-level error info

    # TODO: birds are not required but if provided, should be validated
    if not json.get('date') or\
       not json.get('location') or\
       not json.get('timeofday') or\
       not json.get('hunters'):
        raise BadRequestError('Missing required information')


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

    hunt = session.query(Hunt).get(id)
    if not hunt:
        raise NotFoundError('No hunt found with id %s' % (id))

    huntSchema = HuntSchema()
    return dbResultsToSchemaObjects(hunt, huntSchema)


@app.route('/hunts/{id}/birds', methods=['GET'])
def getBirdsForHunt(id):
    session = _Session()

    hunt = session.query(Hunt).get(id)
    if not hunt:
        raise NotFoundError('No hunt found with id %s' % (id))

    birds = session.query(Bird).filter(Bird.Hunt_id == id)
    birdSchema = BirdSchema()
    return dbResultsToSchemaObjects(birds, birdSchema)


@app.route('/hunts', methods=['POST'])
def addHunt():
    session = _Session()

    request = app.current_request
    json = request.json_body
    validateHuntRequestBody(json)

    # Get referenced Hunter objects
    hunters = session.query(Hunter).filter(
        Hunter.id.in_(json.get('hunters'))).all()

    if not hunters or (len(hunters) != len(json.get('hunters'))):
        raise NotFoundError('One or more specified hunters does not exist')

    # Build up Bird entries
    birds = []
    for bird in json.get('birds'):
        birds.append(Bird(species=bird.get('species'),
                          gender=bird.get('gender'),
                          lost=bird.get('lost'),
                          banded=bird.get('banded'),
                          mounted=bird.get('mounted')))

    # Construct Hunt entries
    hunt = Hunt(date=datetime.strptime(json.get('date'), '%Y-%m-%d'),
                location=json.get('location'),
                timeofday=json.get('timeofday'),
                hunters=hunters,
                birds=birds)

    session.add(hunt)
    session.commit()

    huntSchema = HuntSchema()
    return dbResultsToSchemaObjects(hunt, huntSchema)


@app.route('/hunts/{id}', methods=['PUT'])
def updateHunt(id):
    session = _Session()

    request = app.current_request
    json = request.json_body
    validateHuntRequestBody(json)

    # Get referenced Hunter objects
    hunters = session.query(Hunter).filter(
        Hunter.id.in_(json.get('hunters'))).all()

    if not hunters or (len(hunters) != len(json.get('hunters'))):
        raise NotFoundError('One or more specified hunters does not exist')

    # Build up Bird entries
    birds = []
    for bird in json.get('birds'):
        birds.append(Bird(species=bird.get('species'),
                          gender=bird.get('gender'),
                          lost=bird.get('lost'),
                          banded=bird.get('banded'),
                          mounted=bird.get('mounted')))

    hunt = session.query(Hunt).get(id)
    hunt.date = datetime.strptime(json.get('date'), '%Y-%m-%d')
    hunt.location = json.get('location')
    hunt.timeofday = json.get('timeofday')
    hunt.hunters = hunters
    hunt.birds = birds

    session.commit()


@app.route('/hunts/{id}', methods=['DELETE'])
def deleteHunt(id):
    session = _Session()

    hunt = session.query(Hunt).get(id)
    if not hunt:
        raise NotFoundError('No hunt found with id %s' % (id))

    huntHunterEntries = session.query(HuntHunter)\
                               .filter(HuntHunter.hunt_id == id)\
                               .all()
    for entry in huntHunterEntries:
        session.delete(entry)

    session.delete(hunt)
    session.commit()


@app.route('/birds', methods=['GET'])
def getBirds():
    birdSchema = BirdSchema()
    return getAllResources(Bird, birdSchema)


@app.route('/hunters', methods=['GET'])
def getHunters():
    hunterSchema = HunterSchema()
    return getAllResources(Hunter, hunterSchema)
