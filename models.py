from os import environ
from datetime import datetime

from peewee import *
from flask_login import UserMixin
from dsnparse import parse_environ

if(environ.get('DATABASE_URL')):
    url = parse_environ('DATABASE_URL')
    db = PostgresqlDatabase(url.paths[0], user=url.username, password=url.password,
                            host=url.host, port=url.port)
else:
    db = SqliteDatabase('groovin.db')


class Promoter(Model, UserMixin):
    name = CharField()
    email = CharField(unique=True)
    bio = TextField()
    password = CharField()

    class Meta:
        database = db


class Event(Model):
    name = CharField()
    category = CharField()
    date_time = DateTimeField()
    address = CharField()
    description = TextField()
    image_url = CharField(null=True)
    promoter = ForeignKeyField(Promoter, backref='events', on_delete='CASCADE')

    class Meta:
        database = db


class Ticket(Model):
    name = CharField()
    event = ForeignKeyField(Event, backref='tickets', on_delete='CASCADE')
    price = DecimalField()
    total = IntegerField()

    class Meta:
        database = db


class Order(Model):
    cellphone = CharField()
    ticket = ForeignKeyField(Ticket, backref='orders', on_delete='CASCADE')
    total = IntegerField()

    class Meta:
        database = db


if __name__ == '__main__':
    db.create_tables([Promoter, Event, Ticket, Order, ])
    from services import create_promoter, generate_hash

    create_promoter(name='Dássone J. Yotamo', email='dyotamo@gmail.com',
                    bio='A nice guy online.', password=generate_hash('admin'))
