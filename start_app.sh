#!/bin/sh
set -ex

# Start the Celery worker and Flask application
python3 -m celery -A nad_ch.infrastructure.task_queue worker --loglevel=INFO &
exec python nad_ch/main.py serve_flask_app
