import collections
from chalice import BadRequestError


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


def getAllResources(session, model, schema):
    items = session.query(model).all()
    return dbResultsToSchemaObjects(items, schema)


def validateHuntRequestBody(json):
    if not isinstance(json, dict):
        raise BadRequestError(
            'Invalid body - endpoint accepts single hunt JSON object')

    # TODO: Make this more specific so you know
    # what's missing or maybe this should be some schema check
    # and include field-level error info

    # TODO: birds are not required but if provided, should be validated
    if not json.get('date') or\
       not json.get('location') or\
       not json.get('timeofday') or\
       not json.get('hunters'):
        raise BadRequestError('Missing required information')


def validateHunterRequestBody(json):
    if not isinstance(json, dict):
        raise BadRequestError(
            'Invalid body - endpoint accepts single hunter JSON object')

    if not json.get('firstname'):
        raise BadRequestError('Missing firstname')

    if not json.get('lastname'):
        raise BadRequestError('Missing lastname')
