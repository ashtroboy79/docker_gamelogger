from crypt import methods
from wsgiref import validate
from application import app, db
from application.models import Game, Gamer
from flask import redirect, render_template, url_for, request
from application.forms import gamerForm, gameForm

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/gamers')
def gamers():
    gamer = Gamer.query.all()
    return render_template('gamer.html', gamers=gamer)

@app.route('/gamers/add', methods=['GET', 'POST'])
def add_gamer():
    form = gamerForm()
    if form.validate_on_submit():
        name = form.name.data
        gamer = Gamer(name=name)
        db.session.add(gamer)
        db.session.commit()
        return redirect(url_for('gamers'))
    return render_template('gamer_add.html', form=form, page_header='Add gamer')

@app.route('/gamers/update/<int:id>', methods=['GET','POST'])
def update_gamer(id):
    gamer_to_update = Gamer.query.get_or_404(id)
    form = gamerForm(name=gamer_to_update.name)
    if form.validate_on_submit():
        gamer_to_update.name = form.name.data
        db.session.commit()
        return redirect(url_for('gamers'))
    return render_template('gamer_add.html', form=form, page_header='Update gamer')
    
@app.route('/games')
def games():
    games = Game.query.all()
    return render_template('games.html', games=games)

@app.route('/games/add', methods=['GET', 'POST'])
def add_game():
    form = gameForm()
    gamers = Gamer.query.all()
    for gamer in gamers:
        form.gamer_id.choices.append((gamer.id,f"{gamer.name}"))
    if form.validate_on_submit():
        game = form.name.data
        designer = form.designer.data
        genre = form.genre.data
        rating = form.rating.data
        gamer_id = form.gamer_id.data
        new_game = Game(name=game, designer=designer, genre=genre, rating=rating, gamer_id=gamer_id)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('games'))
    return render_template('game_add.html', form=form, page_header='Add Game')

@app.route('/games/update/<int:id>', methods=['GET','POST'])
def update_game(id):
    game = Game.query.get_or_404(id)
    gamers = Gamer.query.all()
    form = gameForm(name=game.name, designer=game.designer,
                    genre=game.genre, rating=game.rating, gamer_id=game.gamer_id)
    for gamer in gamers:
        form.gamer_id.choices.append((gamer.id,f"{gamer.name}"))
    
    if form.validate_on_submit():
        game.name = form.name.data
        game.designer = form.designer.data
        game.genre = form.genre.data
        game.rating = form.rating.data
        game.gamer_id = form.gamer_id.data
        db.session.commit()
        return redirect(url_for('games'))
    return render_template('game_add.html', form=form, page_header='Update game')

@app.route('/games/delete/<int:id>', methods=['POST'])
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('games'))

@app.route('/gamers/delete/<int:id>', methods=['POST'])
def delete_gamer(id):
    gamer = Gamer.query.get_or_404(id)
    games = Game.query.filter_by(gamer_id=id).all()
    for game in games:
        db.session.delete(game)
        db.session.commit()
    db.session.delete(gamer)
    db.session.commit()
    return redirect(url_for('gamers'))

@app.route('/gamers/<int:id>')
def single_gamer(id):
    gamer = Gamer.query.get_or_404(id)
    games = Game.query.filter_by(gamer_id=id).all()
    return render_template('games.html', games=games, gamer=gamer)

@app.route('/games/designer/<string:designer>')
def games_by_designer(designer):
    games = Game.query.filter_by(designer=designer).all()
    return render_template('games.html', games=games, designer=designer)

@app.route('/games/genre/<string:genre>')
def games_by_genre(genre):
    games = Game.query.filter_by(genre=genre).all()
    return render_template('games.html', games=games, genre=genre)
