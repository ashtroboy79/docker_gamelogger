from application import db

class Gamer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    games = db.relationship('Game', backref='gamerbr')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    designer = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    gamer_id = db.Column(db.Integer, db.ForeignKey('gamer.id'), nullable=False)
