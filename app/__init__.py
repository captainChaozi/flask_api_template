from flask import Flask, g
from app.ext_init import db, get_session, cache,spec
from app.resource import resource_register
from config import Config
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
    resource_register(Api(flasker),spec)
    return flasker


app = create_app()


@app.before_request
def create_session():
    g.db_session = get_session()


@app.shell_context_processor
def make_shell_context():
    return dict(db_session=get_session())
