#!/usr/bin/bash
if [ "$RUN" = "celery" ]; then
    celery -A  task.celery worker -B --loglevel=info
else
    gunicorn run:app --worker-class gevent -b 0.0.0.0:8000 -w 9 --log-level info
fi


