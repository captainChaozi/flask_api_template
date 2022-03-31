from app import app
from ext import make_celery

celery = make_celery(app)
