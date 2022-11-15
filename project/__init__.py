from flask import Flask
from flask_cors import CORS

from . import model, route, schema


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("config.Config")
    model.init_app(app)
    route.init_app(app)
    schema.init_app(app)
    return app
