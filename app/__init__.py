from flask import Flask
from app.ext_init import db, docs, ma, cors, migrate, get_session
from config import Config
from .model import Author, Book


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


@app.shell_context_processor
def make_shell_context():
    return dict(db_session=get_session())
