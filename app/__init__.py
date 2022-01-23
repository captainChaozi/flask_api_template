import logging

from flask import Flask, g
from app.ext_init import db, get_session, cache
from config import Config
from .resource import register_api
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api


def create_app():
    flasker = Flask(__name__)
    flasker.config.from_object(Config)
    cache.init_app(flasker)
    db.init_app(flasker)
    Marshmallow(flasker)
    CORS(flasker)
    Migrate(flasker, db)
    register_api(Api(flasker))
    return flasker


app = create_app()


@app.before_request
def create_session():
    g.db_session = get_session()


@app.shell_context_processor
def make_shell_context():
    return dict(db_session=get_session())


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
