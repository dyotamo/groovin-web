from peewee import SqliteDatabase
from models import Promoter, Event, Ticket, Order


def create_db():
    db = SqliteDatabase(':memory:')

    Promoter.bind(db)
    Event.bind(db)
    Ticket.bind(db)
    Order.bind(db)

    db.create_tables([Promoter, Event, Ticket, Order])
