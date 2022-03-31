from flask_sqlalchemy import SQLAlchemy

from ext import BaseModel, RedisCache
from ext import Docs

db = SQLAlchemy(model_class=BaseModel)

cache = RedisCache()

docs = Docs()




def get_session():
    return db.create_scoped_session(options=dict(autocommit=True, autoflush=False))
