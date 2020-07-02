from os import environ

from flask_login import UserMixin
from dsnparse import parse_environ
from peewee import (SqliteDatabase, PostgresqlDatabase, Model, CharField,
                    TextField, DateTimeField, ForeignKeyField, DecimalField,
                    IntegerField,)

if(environ.get('DATABASE_URL')):
    url = parse_environ('DATABASE_URL')
    db = PostgresqlDatabase(url.paths[0],
                            user=url.username,
                            password=url.password,
                            host=url.host,
                            port=url.port)
else:
    db = SqliteDatabase('groovin.db')


class Promoter(Model, UserMixin):
    name = CharField()
    email = CharField(unique=True)
    bio = TextField()
    password = CharField()

    def to_map(self):
        data = self.__dict__['__data__']
        data.pop('password')
        return data

    class Meta:
        database = db


class Event(Model):
    name = CharField()
    category = CharField()
    date_time = DateTimeField()
    address = CharField()
    description = TextField()
    image_url = CharField(null=True)
    promoter = ForeignKeyField(Promoter,
                               backref='events',
                               on_delete='CASCADE')

    def to_map(self):
        data = self.__dict__['__data__']
        data['date_time'] = data['date_time'].strftime('%d/%m/%Y, %H:%M:%S')
        return data

    class Meta:
        database = db


class Ticket(Model):
    name = CharField()
    event = ForeignKeyField(Event,
                            backref='tickets',
                            on_delete='CASCADE')
    price = DecimalField()
    total = IntegerField()

    class Meta:
        database = db


class Order(Model):
    cellphone = CharField()
    ticket = ForeignKeyField(Ticket,
                             backref='orders',
                             on_delete='CASCADE')
    total = IntegerField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.create_tables([Promoter, Event, Ticket, Order, ])
    from services.promoter import create_promoter
    from werkzeug.security import generate_password_hash

    create_promoter(name='Dássone J. Yotamo',
                    email='dyotamo@gmail.com',
                    bio='A nice guy online.',
                    password=generate_password_hash('admin'))
