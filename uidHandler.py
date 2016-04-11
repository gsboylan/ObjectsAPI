from flask import jsonify, request, make_response, abort

import server

def getSpecificUid(uid, storedObjects):
    """Attempts to find the specified uid in a dict of stored objects, and returns the resulting
    value as JSON.

    Args:
        uid: string used to identify an object in storedObjects

        storedObjects: dict with string keys, containing representations of JSON objects

    Returns:
        Json formatted HTTP response: the specified object if found, or a 404 error otherwise.
    """

    if (uid not in storedObjects):
        abort(404)

    return make_response(jsonify(storedObjects[uid]), 200)

def putObject(uid, storedObjects):
    """Replaces the stored object specified by the uid with a new object constructed using the
    request data. Does not assume that the request data will resemble the original data. Does not
    retain any of the original object's fields aside from uid after replacement.

    Args:
        uid: string used to identify an object in storedObjects

        storedObjects: dict with string keys, containing representations of JSON objects

    Returns:
        Json formatted HTTP response: The updated object if the uid is found, else a 404 error.
    """

    if (uid not in storedObjects):
        abort(404)

    replacementObject = request.json
    replacementObject["uid"] = uid
    storedObjects[uid] = replacementObject

    return make_response(jsonify(replacementObject), 200)

def deleteObject(uid, storedObjects):
    """Deletes an object specified by the uid, if it is found.

    Args:
        uid: String used to identify an object in storedObjects

        storedObjects: dict with string keys, containing representations of JSON objects

    Returns:
        Empty HTTP response regardless of success.
    """

    if uid in storedObjects:
        del storedObjects[uid]

    return make_response('', 204)
