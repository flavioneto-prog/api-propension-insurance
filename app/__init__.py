from flask import Flask
from .extensions.extensions import api
from .controllers.propension import namespace

def create_app():
    app = Flask(__name__)
    api.init_app(app)
    api.add_namespace(namespace, '/v1')
    return app