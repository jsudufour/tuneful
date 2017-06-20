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

@app.route("/api/files", methods=["POST"])
@decorators.accept("application/json")
def files_post():
    """ Add a new song file """
    data = request.json

    # Add the file to the database
    file = database.File(name="")

    session.add(file)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(file.as_dictionary())
    headers = {"Location": url_for("files_post", id=file.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")


@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def songs_post():
    """ Add a new song """
    data = request.json

    # Add the song to the database
    song = database.Song()

    session.add(song)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("songs_post", id=song.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")


@app.route("/api/songs/<int:id>/delete", methods=["DELETE"])
@decorators.accept("application/json")
def song_delete(id):
    """ Delete an existing song """
    # Get post from the database
    song = session.query(database.Song).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not song:
        message = "Could not find song with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Get the supplied JSON for the new post
    data = request.json

    # Edit post and commit to database
    session.query(database.Song).delete(song)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")



@app.route("/api/songs/<int:id>/edit", methods=["PUT"])
@decorators.accept("application/json")
def songs_edit(id):
    """ Edit an existing song """
    # Get post from the database
    song = session.query(database.Song).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not song:
        message = "Could not find song with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Get the supplied JSON for the new post
    data = request.json

    # Edit post and commit to database
    session.query(database.Song).update({'name': data["name"]})
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
