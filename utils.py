from cloudinary.uploader import upload
from flask import request, url_for

from models import Event
from constants import ALLOWED_EXTENSIONS


def view_event_dlc(*args, **kwargs):
    event_id = request.view_args['event_id']
    event = Event.get(event_id)
    return [{'text': event.name, 'url': url_for('event', event_id=event.id)}]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_photo(image):
    return upload(image)['secure_url']
