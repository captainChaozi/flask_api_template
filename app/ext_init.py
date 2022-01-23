from ext import BaseModel,RedisCache
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy(model_class=BaseModel)
cors = CORS()
ma = Marshmallow()
migrate = Migrate()
cache = RedisCache()

def get_session():
    return db.create_scoped_session(options=dict(autocommit=True, autoflush=False))
