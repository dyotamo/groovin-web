from werkzeug.security import check_password_hash
from models import Promoter


def create_promoter(**kwargs):
    return Promoter.create(**kwargs)


def get_promoter(promoter_id):
    return Promoter[promoter_id]


def check_promoter(email, password):
    try:
        promoter = Promoter.select().where(Promoter.email == email).get()
        if check_password_hash(promoter.password, password):
            return promoter
    except Promoter.DoesNotExist:
        pass
