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
@decorators.accept("application/json")
def files_get():
    """ Get all files as json """
    songs = session.query(database.Song)

    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

# @app.route("/api/files", methods=["POST"])
# @decorators.accept("application/json")

@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def songs_post():
    """ Add a new song file """
    data = request.json

    # Add the song to the database
    song = database.Song()

    session.add(song)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
