from flask import request, url_for
from models import Event


def view_event_dlc(*args, **kwargs):
    event_id = request.view_args['event_id']
    event = Event.get(event_id)
    return [{'text': event.name, 'url': url_for('event', event_id=event.id)}]
