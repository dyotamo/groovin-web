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
    password = CharField()

    class Meta:
        database = db


class Event(Model):
    name = CharField()
    category = CharField()
    date_time = DateTimeField()
    promoter = ForeignKeyField(Promoter, backref='events')

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([Promoter, Event, ])
    from services import create_promoter

    create_promoter(name='Dássone J. Yotamo',
                    email='dyotamo@gmail.com')
