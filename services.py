from datetime import datetime

from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

from models import Promoter, Event


def create_promoter(name, email, password='admin'):
    Promoter.create(name=name, email=email,
                    password=generate_password_hash(password))


def get_promoter(promoter_id):
    return Promoter[promoter_id]


def check_promoter(email, password):
    try:
        promoter = Promoter.select().where(Promoter.email == email).get()
        if check_password_hash(promoter.password, password):
            return promoter
    except Promoter.DoesNotExist:
        pass


def get_events():
    return current_user.events


def create_event(name, category, description,  image_url, date_time=datetime.now()):
    Event.create(name=name, category=category,
                 date_time=date_time, description=description, promoter=current_user.id, image_url=image_url)


def get_event(event_id):
    try:
        return Event[event_id]
    except Event.DoesNotExist:
        pass


def check_object(obj):
    if obj is None:
        return abort(404)
