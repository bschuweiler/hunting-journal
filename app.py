from chalice import Chalice, BadRequestError, NotFoundError, Response
from datetime import datetime
from sqlalchemy import create_engine, extract
from sqlalchemy.orm import sessionmaker
from chalicelib.orm import (
    Base, Hunt, Bird, Hunter, HuntHunter,
    HuntSchema, BirdSchema, HunterSchema, HuntHunterSchema
)
from chalicelib.controller_utils import *


_db = 'sqlite:///testdata.db'
_dbEngine = create_engine(_db)
_Session = sessionmaker(bind=_dbEngine)

app = Chalice(app_name='hunting-journal')
app.debug = True

# TODO: Tests
# TODO: Swagger
# TODO: Check for injection issues
# TODO: Clean up imports, make requirements.txt accurate
# TODO: Some backup option for yearly dumps to csv or something
# or just be comfortable with format + RDS replicas?
# TODO: Externalize config like _db - sqlite for local, RDS for lambda
# TODO: Authentication? (or just defer to hosting w/AWS and API Gateway front?)
# TODO: HTTP caching ETag or Last-Modified w/ 304, etc. when appropriate
# TODO: Hypermedia or at least a better index route with available endpoints?


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

    birdSchema = BirdSchema()
    return dbResultsToSchemaObjects(hunt.birds, birdSchema)


@app.route('/hunts/{id}/hunters', methods=['GET'])
def getHuntersForHunt(id):
    session = _Session()

    hunt = session.query(Hunt).get(id)
    if not hunt:
        raise NotFoundError('No hunt found with id %s' % (id))

    hunterSchema = HunterSchema()
    return dbResultsToSchemaObjects(hunt.hunters, hunterSchema)


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


@app.route('/birds/{id}', methods=['GET'])
def getBird(id):
    session = _Session()

    bird = session.query(Bird).get(id)
    if not bird:
        raise NotFoundError('No bird found with id %s' % (id))

    birdSchema = BirdSchema()
    return dbResultsToSchemaObjects(bird, birdSchema)


@app.route('/hunters', methods=['GET'])
def getHunters():
    session = _Session()

    hunterSchema = HunterSchema()
    return getAllResources(session, Hunter, hunterSchema)


@app.route('/hunters/{id}', methods=['GET'])
def getHunter(id):
    session = _Session()

    hunter = session.query(Hunter).get(id)
    if not hunter:
        raise NotFoundError('No hunter found with id %s' % (id))

    hunterSchema = HunterSchema()
    return dbResultsToSchemaObjects(hunter, hunterSchema)


@app.route('/hunters', methods=['POST'])
def addHunter():
    session = _Session()

    request = app.current_request
    json = request.json_body
    validateHunterRequestBody(json)

    existingHunters = session.query(Hunter).\
        filter(Hunter.firstname == json.get('firstname'),
               Hunter.lastname == json.get('lastname')).all()

    if len(existingHunters) > 0:
        raise BadRequestError("Specified hunter already exists")

    hunter = Hunter(firstname=json.get('firstname'),
                    lastname=json.get('lastname'))

    session.add(hunter)
    session.commit()

    hunterSchema = HunterSchema()
    return dbResultsToSchemaObjects(hunter, hunterSchema)


@app.route('/hunters/{id}', methods=['PUT'])
def updateHunter(id):
    session = _Session()

    request = app.current_request
    json = request.json_body
    validateHunterRequestBody(json)

    hunter = session.query(Hunter).get(id)
    hunter.firstname = json.get('firstname')
    hunter.lastname = json.get('lastname')

    session.commit()
