from flask import Flask, g
from app.ext_init import db, ma, cors, migrate, get_session, cache
from config import Config
from .model import Author, Book
from .resource import AuthorListResource, register_api


def create_app():
    flasker = Flask(__name__)
    flasker.config.from_object(Config)
    cache.init_app(flasker)
    db.init_app(flasker)
    ma.init_app(flasker)
    cors.init_app(flasker)
    migrate.init_app(flasker, db)
    register_api(flasker)
    return flasker


app = create_app()


@app.before_request
def create_session():
    g.db_session = get_session()


@app.shell_context_processor
def make_shell_context():
    return dict(db_session=get_session())
