from datetime import datetime

from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

from models import db, Promoter, Event, Ticket
from utils import upload_photo


def generate_hash(passwd):
    return generate_password_hash(passwd)


def create_promoter(**kwargs):
    Promoter.create(**kwargs)


def get_promoter(promoter_id):
    return Promoter[promoter_id]


def check_promoter(email, password):
    try:
        promoter = Promoter.select().where(Promoter.email == email).get()
        if check_password_hash(promoter.password, password):
            return promoter
    except Promoter.DoesNotExist:
        pass


def create_event(**kwargs):
    return Event.create(promoter=current_user.id, **kwargs)


def get_event(event_id):
    try:
        return Event[event_id]
    except Event.DoesNotExist:
        return abort(404)


def remove_event(event):
    event.delete_instance()


def update_event(event, data):
    image = _remove_csrf_token_and_image_fields(data)
    Event.update(image_url=upload_photo(image), **
                 data).where(Event.id == event.id).execute()


def _remove_csrf_token_and_image_fields(data):
    data.pop('csrf_token')
    return data.pop('image')


def create_ticket(**kwargs):
    Ticket.create(**kwargs)
