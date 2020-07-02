from os.path import join
from datetime import datetime

from cloudinary.uploader import upload
from flask import request, url_for
from werkzeug.utils import secure_filename

from models import Event


def remove_csrf_token_and_image_fields(data):
    data.pop('csrf_token')
    return data.pop('image')


def view_event_dlc(*args, **kwargs):
    event_id = request.view_args['event_id']
    event = Event.get(event_id)
    return [{'text': event.name, 'url': url_for('web.event', event_id=event.id)}]


def upload_photo(image):
    if image is not None:
        image_path = join('/tmp', secure_filename(image.filename))
        image.save(join(image_path))  # tmp save
        return upload(image_path)['secure_url']


def is_valid_date_time(date_time):
    return date_time > datetime.now()


def ticket_already_added(event, kind):
    return any(ticket.name == kind for ticket in event.tickets)
