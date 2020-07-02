from flask import Blueprint
from flask_restful import Api, Resource

from services.event import all_events, get_event
from services.promoter import get_promoter

api = Blueprint('api', __name__, url_prefix='/api')
app = Api(api)


class EventList(Resource):
    def get(self):
        return [event.to_map() for event in all_events()]


class EventDetails(Resource):
    def get(self, event_id):
        return get_event(event_id).to_map()


class PromoterDetails(Resource):
    def get(self, promoter_id):
        return get_promoter(promoter_id).to_map()


app.add_resource(EventList, '/events')
app.add_resource(EventDetails, '/events/<int:event_id>')
app.add_resource(PromoterDetails, '/promoters/<int:promoter_id>')
