import pytest
import database.tables
from database.dbconfig import Database
import flask_testing as ftest
from config import app, tunnel

db = Database.setup(app, tunnel, True)

class MyTest(ftest.TestCase):

    def create_app(self):
        return app

    def setUp(self):
