#/bin/bash

poetry run celery -A nad_ch.infrastructure.task_queue worker --loglevel=INFO & poetry run start-web
