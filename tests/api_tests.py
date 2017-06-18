import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import database
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    # def test_unsupported_accept_header(self):
    #     response = self.client.get("/api/songs",
    #         headers=[("Accept", "application/xml")]
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.mimetype, "application/xml")
    #
    #     data = json.loads(response.data.decode("ascii"))
    #     self.assertEqual(data["message"],
    #                      "Request must accept application/xml data")

    def test_get_empty_file(self):
        """Getting a file from an empty database"""
        response = self.client.get("/api/songs",
            headers=[("Accept", "application/xml")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/xml")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])

    def test_get_file(self):
        """Getting a single file"""
        songA = database.Song()
        fileA = database.File(name="justasong.mp3")
        songA.file = fileA

        session.add_all([songA, fileA])
        session.commit()

        response = self.client.get("/api/songs",
            headers=[("Accept", "application/xml")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/xml")

        data = json.loads(response.data.decode("ascii"))

        song = data[0]
        self.assertEqual(song["file"], fileA.as_dictionary())

    def test_get_all_files(self):
        """Getting a list of all songs as json"""
        songA = database.Song()
        fileA = database.File(name="justasong.mp3")
        songA.file = fileA

        songB = database.Song()
        fileB = database.File(name="justanothersong.mp3")
        songB.file = fileB

        songC = database.Song()
        fileC = database.File(name="justonemoresong.mp3")
        songC.file = fileC

        session.add_all([songA, fileA, songB, fileB, songC, fileC])
        session.commit()

        response = self.client.get("/api/songs",
            headers=[("Accept", "application/xml")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/xml")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 3)

        songA = data[0]
        self.assertEqual(songA["file"], fileA.as_dictionary())

        songB = data[1]
        self.assertEqual(songB["file"], fileB.as_dictionary())

        songC = data[2]
        self.assertEqual(songC["file"], fileC.as_dictionary())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())
