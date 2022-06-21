from application import db
from application.models import Gamer, Game

if __name__ == '__main__':
    db.drop_all()
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
 