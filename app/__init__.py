from flask import Flask, g
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api

from app.ext_init import db, get_session, cache, docs
from app.resource import resource_register
from app.script import script
from config import Config


def create_app():
    flasker = Flask(__name__)
    flasker.config.from_object(Config)
    docs.init_app(flasker)
    cache.init_app(flasker)
    db.init_app(flasker)
    Marshmallow(flasker)
    Migrate(flasker, db)
    resource_register(Api(flasker))
    CORS(flasker, supports_credentials=True)
    return flasker


app = create_app()
app.cli.add_command(script)


@app.before_request
def create_session():
    g.db_session = get_session()


@app.shell_context_processor
def make_shell_context():
    return dict(db_session=get_session())
