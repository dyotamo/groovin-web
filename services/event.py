from flask import abort
from flask_login import current_user

from models import Event
from utils import (upload_photo, is_valid_date_time,
                   remove_csrf_token_and_image_fields)


def create_event(**kwargs):
    if is_valid_date_time(kwargs['date_time']):
        return True, Event.create(promoter=current_user.id, **kwargs)
    return False, 'A data informada é superior a data actual.'


def get_event(event_id):
    try:
        return Event[event_id]
    except Event.DoesNotExist:
        return abort(404)


def remove_event(event):
    event.delete_instance()


def update_event(event, data):
    image = remove_csrf_token_and_image_fields(data)
    if is_valid_date_time(data['date_time']):
        Event.update(image_url=upload_photo(image), **
                     data).where(Event.id == event.id).execute()
        return True, None
    return False, 'A data informada é superior a data actual.'
