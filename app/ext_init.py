from ext import BaseModel
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy(model_class=BaseModel)
docs = FlaskApiSpec()
cors = CORS()
ma = Marshmallow()
migrate = Migrate()


def get_session():
    return db.create_scoped_session(options=dict(autocommit=True, autoflush=False))
