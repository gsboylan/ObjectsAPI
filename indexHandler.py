from flask import url_for, jsonify, request, make_response, abort
from uuid import uuid4

import server

def getUidList(storedObjects):
    """Produces a list of URLs which can be used to view the details of the stored objects.

    Args:
        storedObjects: dict with string keys, containing representations of JSON objects. URLs will
            be produced for the values in this dict.

    Returns:
        Json formatted object: contains a single field 'objects' which is a list of Json objects,
            each containing a field 'url' which contains the URL of a stored object.
    """

    objectList = []
    for uid in storedObjects.keys():
        responseObject = {"url": url_for('handleUidRoute', uid=uid, _external=True)}
        objectList.append(responseObject)

    return make_response(jsonify(objects=objectList), 200)

def postObject(storedObjects):
    """Adds Json objects to the stored object dict. Handles single objects, or lists of objects.

    Args:
        storedObjects: dict with string keys, containing representations of JSON objects. New
            objects will be added to this dict.

    Returns:
        The new objects produced, including their new uids. If multiple objects are added, a list is
            returned.
    """

    if isinstance(request.json, dict):
        newObject = request.json
        uid = str(uuid4())
        newObject["uid"] = uid
        storedObjects[uid] = newObject
        return make_response(jsonify(newObject), 201)

    elif isinstance(request.json, list):
        newObjects = []

        for item in request.json:
            uid = str(uuid4())
            item["uid"] = uid
            storedObjects[uid] = item
            newObjects.append(item)

        return make_response(jsonify(objects=newObjects), 201)

    abort(400)
