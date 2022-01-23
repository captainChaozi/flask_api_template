from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        broker_url=app.config["CELERY_BROKER_URL"],
        timezone="Asia/Shanghai",
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        beat_schedule=app.config["CELERY_BEAT_SCHEDULE"],
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
