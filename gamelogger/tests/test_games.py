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
        bob = Gamer(name='Bob')
        ben = Gamer(name='Ben')
        joe = Gamer(name='Joe')
        game1 = Game(name='Argent The Consortium', designer='Trey Chambers', genre='Fantasy', rating=0, gamerbr=bob)
        game2 = Game(name="Revolution", designer='Steve Jackson', genre='Bluffing', rating=0, gamerbr=bob)
        game3 = Game(name='Neanderthal', designer='Phil Enklund', genre='Tableu Building', rating=0, gamerbr=ben)
        game4 = Game(name='Greenland', designer='Phil Enklund', genre='Tableu Building', rating=0, gamerbr=joe)
        db.session.add_all([bob,ben,joe,game1,game2,game3, game4])
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestDisplayGames(TestBase):
    def test_gamers(self):
        response = self.client.get(url_for('games'))
        self.assert200(response)
        self.assertIn(b'Neanderthal', response.data)
        
class TestAddGames(TestBase):
    def test_add_game(self):
        response = self.client.post(
            url_for('add_game'),
            data = dict(name='Machina Arcana',designer='',genre='',rating=0,  gamer_id=3),
            follow_redirects=True
            )
        self.assert200(response)
        self.assertIn(b'Machina Arcana', response.data)

    def test_add_game_get(self):
        response = self.client.get(url_for('add_game'))
        self.assert200(response)
        self.assertIn(b'Designer', response.data)

class TestUpdateGames(TestBase):
    def test_update_game_get(self):
        response = self.client.get(url_for('update_game', id=1))
        self.assert200(response)
        self.assertIn(b'Argent The Consortium', response.data)
 
    def test_update_game(self):
        response = self.client.post(url_for('update_game', id=1),
                   data = dict(name='Stuffed Fables',designer='',genre='', rating=3, gamer_id=1),
                   follow_redirects=True       
                   )
        self.assert200(response)
        self.assertIn(b'Stuffed Fables', response.data)
        
class TestDeleteGames(TestBase):
    def test_delete_game(self):
        response = self.client.post(url_for('delete_game', id=1),
                   follow_redirects=True
                   )
        self.assert200(response)
        assert Game.query.get(1) is None

class TestDisplayGamesDev(TestBase):
    def test_games_for_designer(self):
        response = self.client.get(url_for('games_by_designer', designer='Steve Jackson'))
        self.assert200(response)
        self.assertIn(b'Revolution', response.data)
        self.assertNotIn(b'Neanderthal', response.data)

    def test_games_for_designer_2(self):
        response = self.client.get(url_for('games_by_designer', designer='Phil Enklund'))
        self.assert200(response)
        self.assertNotIn(b'Revolution', response.data)
        self.assertIn(b'Neanderthal', response.data)
        self.assertIn(b'Greenland', response.data)

class TestDisplayGamesGenre(TestBase):
    def test_games_for_genre(self):
        response = self.client.get(url_for('games_by_genre', genre='Fantasy'))
        self.assert200(response)
        self.assertIn(b'Argent The Consortium', response.data)
        self.assertNotIn(b'Neanderthal', response.data)
