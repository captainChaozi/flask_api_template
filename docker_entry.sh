#!/usr/bin/bash

if [ "$RUN" = "celery" ]; then
    echo "运行celery"
    celery -A  task.celery worker -B --loglevel="${LOG_LEVEL}"

elif [ "$RUN" = "debug" ]; then
    echo "这是调试模式"
    gunicorn run:app -b 0.0.0.0:8000 --log-level debug --reload --log-file app.log
else
    echo "欢迎来到Flask"
    gunicorn run:app --worker-class gevent -b 0.0.0.0:8000 -w 9 --log-level "${LOG_LEVEL}" --log-file app.log
fi


