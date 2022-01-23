from .create_celery import celery

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def send_message():
    logger.warning('这是warning 日志')
    return 'celery is working '


@celery.task
def delay_task(message):
    logger.warning('触发delay')
    return {"message": f"{message}"}
