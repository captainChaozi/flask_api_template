from pprint import pprint
from flask.cli import AppGroup
from app.ext_init import get_session

script = AppGroup("script")


@script.command("init_meta")
def init_meta():
    db_session = get_session()
    pprint('hello')
