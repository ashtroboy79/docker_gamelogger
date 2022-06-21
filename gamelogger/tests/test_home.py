from urllib import response
from flask import url_for, redirect
from flask_testing import TestCase
from application import app, db

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestIndex(TestBase):
    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)
        self.assertIn(b'Welcome to gamelogger', response.data)
