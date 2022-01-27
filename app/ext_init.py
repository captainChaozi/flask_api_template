from ext import BaseModel, RedisCache
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
db = SQLAlchemy(model_class=BaseModel)

cache = RedisCache()



spec = APISpec(
    title="Gisty",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="A minimal gist API"),
    plugins=[MarshmallowPlugin()],
)


def get_session():
    return db.create_scoped_session(options=dict(autocommit=True, autoflush=False))
