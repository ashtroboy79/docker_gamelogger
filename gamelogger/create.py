from application import db
from application.models import Gamer, Game

if __name__ == '__main__':
    db.create_all()
