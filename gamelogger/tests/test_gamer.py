from urllib import response
from flask import url_for, redirect
     
from flask_testing import TestCase
from application import app, db
from application.models import Gamer,Game

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
        bob = Gamer(name='Bob The Builder')
        joe = Gamer(name='Joe Blogs')
        ben = Gamer(name='Ben')
        game1 = Game(name='Argent The Consortium',rating=0, gamerbr=bob)
        game2 = Game(name="Revolution", designer='Steve Jackson',rating=0, gamerbr=bob)
        game3 = Game(name='Neanderthal', rating=0,gamerbr=ben)
        db.session.add_all([bob,joe,ben,game1,game2,game3])
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestAddGamer(TestBase):
    def test_add_gamer(self):
        response = self.client.post(
            url_for('add_gamer'),
            data = dict(name='James Howlett')
            )
        assert list(Gamer.query.filter_by(name='James Howlett').all())[0].id == 4
    
    def test_add_game_get(self):
        response = self.client.get(url_for('add_gamer'))
        self.assert200(response)
        self.assertIn(b'Name', response.data)

class TestDisplayGamer(TestBase):
    def test_gamers(self):
        response = self.client.get(url_for('gamers'))
        self.assert200(response)
        self.assertIn(b'Bob The Builder', response.data)


class TestUpdateGamer(TestBase):
    def test_update_gamer_get(self):
        response = self.client.get(url_for('update_gamer', id=2))
        self.assert200(response)
        self.assertIn(b'Joe Blogs', response.data)
        
    def test_update_gamer(self):
        response = self.client.post(url_for('update_gamer', id=2),
                   data = dict(name="Scott Summers"),
                   follow_redirects=True
                    )
        self.assert200(response)
        self.assertIn(b'Scott Summers', response.data)
        
    
class TestDeleteGamer(TestBase):
    def test_delete_gamer(self):
        response = self.client.post(url_for('delete_gamer', id=1),
                   follow_redirects=True
                   )
        self.assert200(response)
        assert Gamer.query.get(1) is None
        
class TestSortedDisplay(TestBase):
    def test_single_gamer(self):
        response = self.client.get(url_for('single_gamer', id=1))
        self.assert200(response)
        self.assertIn(b'Argent The Consortium', response.data)
        self.assertIn(b'Revolution', response.data)
        self.assertNotIn(b'Neanderthal', response.data)
