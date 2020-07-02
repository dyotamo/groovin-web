from os import environ

from flask_login import LoginManager
from flask_breadcrumbs import Breadcrumbs
from flask import Flask

from constants import LOGIN_MESSAGE
from web import web
from services.promoter import get_promoter

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or 'secret'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = LOGIN_MESSAGE
login_manager.login_message_category = "warning"

breadcrumbs = Breadcrumbs()
breadcrumbs.init_app(app)


app.register_blueprint(web)


@login_manager.user_loader
def load_user(promoter_id):
    return get_promoter(promoter_id)


if __name__ == "__main__":
    app.run(debug=True)
