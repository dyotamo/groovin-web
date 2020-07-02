from models import Ticket


def create_ticket(**kwargs):
    Ticket.create(**kwargs)
