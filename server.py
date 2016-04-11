 #!/usr/bin/python

from flask import Flask, jsonify, request, make_response
from uuid import uuid4
from werkzeug.exceptions import HTTPException
from argparse import ArgumentParser

import uidHandler
import indexHandler

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS']=True
storedObjects = {}

@app.route('/api/objects/', methods=['GET', 'POST'])
def handleIndexRoute():
    """Sends GET and POST requests to the index route to their respective handler methods.
    Rejects other request types and throws a 405 error.

    Returns:
        Json formatted http response.
    """
    if request.method == 'GET':
        return indexHandler.getUidList(storedObjects)
    elif request.method == 'POST':
        return indexHandler.postObject(storedObjects)


@app.route('/api/objects/<string:uid>', methods=['GET', 'PUT', 'DELETE'])
def handleUidRoute(uid):
    """Sends GET, PUT, and DELETE request types to any route with a supplied Id string.
    Rejects other request types and throws a 405 error.

    Args:
        uid: String suffix to the api route.

    Returns:
        Json formatted http response.
    """
    if request.method == 'GET':
        return uidHandler.getSpecificUid(uid, storedObjects)
    elif request.method == 'PUT':
        return uidHandler.putObject(uid, storedObjects)
    elif request.method == 'DELETE':
        return uidHandler.deleteObject(uid, storedObjects)


@app.errorhandler(HTTPException)
def returnError(error):
    """Constructs and returns an error response in JSON.
    Handles all HTTP exceptions as long as TRAP_HTTP_EXCEPTIONS is set to True.

    Args:
        error: flask error type, specifying a description, code, and name.

    Returns:
        Json formatted HTTP response containing the request's type, URL, and an error message.
    """

    errorObject = {
        "verb" : request.method,
        "url" : request.url,
        "message" : str(error.code) +  ': ' + error.name
    }

    return make_response(jsonify(errorObject), error.code)


if __name__ == '__main__':
    parser = ArgumentParser("Launch the API:  python server.py")
    parser.add_argument('-p', '--port',
        type=int,
        help="The port to listen on. Defaults to 5000.",
        default=5000)
    parser.add_argument('-d', '--debug',
        help="Launch the app in debug mode. The server will only be accessible from the local \
            host for security. Defaults to False.",
        default=False,
        action='store_true')
    args = parser.parse_args()

    if args.debug:
        app.run(debug=args.debug, port=args.port)
    else:
        app.run(host="0.0.0.0", port=args.port)
