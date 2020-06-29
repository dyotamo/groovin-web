from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired

_REQUIRED = DataRequired(message="Este campo é obrigatório.")
_CATEGORIES = [('Disco', 'Disco'),
               ('Festival', 'Festival'),
               ('Show', 'Show'),
               ('Outros', 'Outros')]


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[_REQUIRED])
    password = PasswordField('Senha', validators=[_REQUIRED])


class EventForm(FlaskForm):
    name = TextField('Nome', validators=[_REQUIRED])
    category = SelectField('Categoria', choices=_CATEGORIES)
    description = TextAreaField('Descrição', validators=[_REQUIRED])
