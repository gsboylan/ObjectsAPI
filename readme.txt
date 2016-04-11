This server provides a RESTful api (at hostname/api/objects/) which stores arbitrary JSON objects.
The server requires Python 2.

This program requires Flask for python. To install:
    sudo apt-get install python-pip # If not already installed
    sudo pip install flask

Flask installs Werkzeug, Jinja2, itsdangerous, and MarkupSafe as dependencies.

To launch the server:
python server.py [-h] [-p PORT] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  The port to listen on. Defaults to 5000.
  -d, --debug           Launch the app in debug mode. The server will only be
                        accessible from the local host for security. Defaults
                        to False.

To run unit tests: python TestSuite.py
