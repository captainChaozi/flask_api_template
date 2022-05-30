import logging
import os
from datetime import timedelta
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))
page_dir = os.path.join(basedir, 'pages')
pem = os.path.join(basedir, 'pem')


class Config:
    # flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    # 微信
    APP_ID = os.getenv('APP_ID', '***')
    APP_SECRET = os.getenv('APP_SECRET', '***')

    OSS_KEY_ID = os.getenv('OSS_KEY_ID', "")
    OSS_KEY_SECRET = os.getenv('OSS_KEY_SECRET', "")
    OSS_BUCKET = os.getenv('OSS_BUCKET', "")
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', "")
    OSS_DOMAIN = os.getenv('OSS_DOMAIN', "")

    # 支付宝配置

    ALIPAY_APP_ID = os.getenv('ALIPAY_APP_ID', '')
    ALIPAY_PRIVATE_KEY = os.getenv('ALIPAY_PRIVATE_KEY')
    ALIPAY_PUBLIC_KEY = os.getenv('ALIPAY_PUBLIC_KEY')
    ALIPAY_AES = os.getenv('ALIPAY_AES', '')

    # sqlalchemy配置
    user = os.getenv('DB_USER', 'chaozi')
    pwd = os.getenv('DB_PASSWORD', 'Dream001$')
    host = os.getenv('DB_HOST', '124.221.131.183')
    port = os.getenv('DB_PORT', '20103')
    db = os.getenv('DB_NAME', 'chaozi')
    data = dict(user=user, pwd=pwd, host=host, port=port, db=db)
    con_str = 'postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}'
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL') or con_str.format(**data)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis 配置
    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_DB = os.getenv('REDIS_DB', 0)
    _redis_url = "redis://{host}:{port}/{db}". \
        format(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    # celery 配置
    CELERY_BROKER_URL = _redis_url
    CELERY_RESULT_BACKEND = _redis_url
    CELERY_BEAT_SCHEDULE = {
        'send_message': {
            # 这里想要定期执行的函数路径
            'task': 'task.task_example.send_message',
            "schedule": timedelta(seconds=60),
        },
        # "send_message": {
        #     "task": "task.task_example.send_message",
        #     "schedule": crontab(minute=10, hour=8, day_of_week=1)
        # },
    }

    # 日志配置
    logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s %(lineno)d: %(message)s')
    DOCS_CONFIG = dict(title="**API文档",
                       version="1.0.0",
                       openapi_version="3.0.2",
                       info=dict(description="**API"),
                       servers=[dict(
                           url="http://dev-url.com",
                           description="dev api"
                       )]
                       )
