import os
import logging
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
docs_file = os.path.join(basedir, 'docs', 'api.yaml')


class Config:
    # flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    # 文档配置

    APISPEC_SWAGGER_URL = '/swagger/'

    # 微信
    APP_ID = os.getenv('APP_ID', '***')
    APP_SECRET = os.getenv('APP_SECRET', '***')

    OSS_KEY_ID = os.getenv('OSS_KEY_ID', "***")
    OSS_KEY_SECRET = os.getenv('OSS_KEY_SECRET', "***")
    OSS_BUCKET = os.getenv('OSS_BUCKET', "***")
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', "****")
    OSS_DOMAIN = os.getenv('OSS_DOMAIN', "****")

    # 支付宝配置

    ALIPAY_APP_ID = os.getenv('ALIPAY_APP_ID', '*****')
    ALIPAY_PRIVATE_KEY = os.getenv('ALIPAY_PRIVATE_KEY', '***')
    ALIPAY_PUBLIC_KEY = os.getenv('ALIPAY_PUBLIC_KEY', '***')
    ALIPAY_AES = os.getenv('ALIPAY_AES', '****')
    ALI_PAY_SERVER_URL = os.getenv('ALI_PAY_SERVER_URL', 'https://openapi.alipay.com/gateway.do')
    ALI_PAY_APP_ID = os.getenv('ALI_PAY_APP_ID', '2021002114633190')
    ALI_PAY_DEBUG = os.getenv('ALI_PAY_DEBUG', False)
    ALI_NOTIFY_URL = os.getenv('ALI_NOTIFY_URL', 'https://newapi.lichidental.com/shop/verify_ali')

    # sqlalchemy配置
    user = os.getenv('DB_USER', 'postgres')
    pwd = os.getenv('DB_PASSWORD', 'postgres')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    db = os.getenv('DB_NAME', 'postgres')
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
        'query_status': {
            # 这里想要定期执行的函数路径
            'task': 'task.task_example.send_message',
            "schedule": timedelta(seconds=60),
        },
    }

    # 日志配置
    logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s %(lineno)d: %(message)s')
