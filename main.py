from os import environ

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_breadcrumbs import Breadcrumbs

from constants import LOGIN_MESSAGE

from apps.web import web
from apps.api import api

from services.promoter import get_promoter

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or 'secret'

login_manager = LoginManager(app)
login_manager.login_view = 'web.login'
login_manager.login_message = LOGIN_MESSAGE
login_manager.login_message_category = "warning"

breadcrumbs = Breadcrumbs(app)


app.register_blueprint(web)
app.register_blueprint(api)


@login_manager.user_loader
def load_user(promoter_id):
    return get_promoter(promoter_id)


@app.errorhandler(404)
def not_found(e):
    resp = jsonify(dict(error="Not Found"))
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)
