from tokenize import Number
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class gamerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField()

class gameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    designer = StringField('Designer', validators=[Length(max=50)])
    genre = StringField('Genre', validators=[Length(max=50)])
    rating = IntegerField('Rating',default=0, validators=[NumberRange(0,10)])
    gamer_id = SelectField('Gamer', choices=[])
    submit = SubmitField()
