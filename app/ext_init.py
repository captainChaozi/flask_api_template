from ext import BaseModel, RedisCache
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(model_class=BaseModel)

cache = RedisCache()



def get_session():
    return db.create_scoped_session(options=dict(autocommit=True, autoflush=False))
