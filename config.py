import os
from datetime import timedelta

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    # 文档配置
    APISPEC_SPEC=APISpec(title=os.getenv('APP_NAME','api'),version='v1',openapi_version='3.0.0',plugins=[MarshmallowPlugin()])

    APISPEC_SWAGGER_URL='/swagger/'

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
    ALIPAY_AES = os.getenv('ALIPAY_AES','****')
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
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis 配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_DB = os.getenv('REDIS_DB', 0)
    _redis_url = "redis://:{host}:{port}/{db}". \
        format(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


    # celery 配置
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_BROKER_URL = _redis_url
    CELERY_RESULT_BACKEND = _redis_url
    CELERYBEAT_SCHEDULE = {
        'query_status': {
            # 这里想要定期执行的函数路径
            'task': 'task.task.send_message',
            "schedule": timedelta(seconds=60),
        },
        # 'update_es': {
        #     # 这里想要定期执行的函数路径
        #     'task': 'task.task.update_es',
        #     "schedule": timedelta(minutes=10),
        # },
        # 'check_u8_order': {
        #     # 这里想要定期执行的函数路径
        #     'task': 'task.task.check_u8_order',
        #     "schedule": timedelta(minutes=10),
        # }
    }
