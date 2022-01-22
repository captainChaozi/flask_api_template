from flask import Flask, g
from app.ext_init import db, docs, ma, cors, migrate, get_session
from config import Config
from .model import Author, Book
from .resource import register_resource


def create_app():
    flasker = Flask(__name__)
    flasker.config.from_object(Config)
    db.init_app(flasker)
    docs.init_app(flasker)
    ma.init_app(flasker)
    cors.init_app(flasker)
    migrate.init_app(flasker, db)
    return flasker


app = create_app()

with app.app_context():
    with app.test_request_context():
        g.db_session = get_session()
        register_resource(app,docs)


@app.before_request
def create_session():
    g.db_session = get_session()


@app.shell_context_processor
def make_shell_context():
    return dict(db_session=get_session())
