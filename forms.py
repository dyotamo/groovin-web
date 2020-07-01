from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.html5 import EmailField, DateTimeField

from wtforms import TextField, PasswordField, TextAreaField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired


_REQUIRED = DataRequired(message="Este campo é obrigatório!")
_IMAGE_ONLY = FileAllowed(['png', 'jpg', 'jpeg'], 'Apenas imagens!')

_EVENT_CATEGORIES = [('Disco', 'Disco'), ('Festival',
                                          'Festival'), ('Show', 'Show'), ('Outros', 'Outros')]

_TICKET_CATEGORIES = [('Normal', 'Normal'), ('VIP', 'VIP'),
                      ('Mulher', 'Mulher'), ('Criança', 'Criança'), ('Outro', 'Outro')]


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[_REQUIRED])
    password = PasswordField('Senha', validators=[_REQUIRED])


class EventForm(FlaskForm):
    name = TextField('Nome', validators=[_REQUIRED])
    category = SelectField('Categoria', choices=_EVENT_CATEGORIES)
    date_time = DateTimeField(
        'Horário', format='%d/%m/%Y', validators=[_REQUIRED])
    address = TextField('Local', validators=[_REQUIRED])
    description = TextAreaField('Descrição', validators=[_REQUIRED])
    image = FileField('Foto', validators=[_IMAGE_ONLY])


class TicketForm(FlaskForm):
    kind = SelectField('Tipo', choices=_TICKET_CATEGORIES)
    price = DecimalField(validators=[_REQUIRED])
    total = IntegerField(validators=[_REQUIRED])
