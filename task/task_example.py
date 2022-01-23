from .create_celery import celery

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def send_message():
    print('corntab 日志')
    return 'celery is working '


@celery.task
def delay_task(message):
    print('delay日志')
    return {"message": f"{message}"}
