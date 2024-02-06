#/bin/bash

poetry run celery -A nad_ch.infrastructure.task_queue worker --loglevel=info & poetry run start-web
