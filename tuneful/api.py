import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import database
from . import decorators
from . import app
from .database import session
from .utils import upload_path


@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/xml")
def files_get():
    """ Get all files as json """
    songs = session.query(database.Song)

    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/xml")
