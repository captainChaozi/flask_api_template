from ext import make_celery
from app import app

celery = make_celery(app)
