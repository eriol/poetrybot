#!/bin/sh

set -e

. /venv/bin/activate

poetrybot &

exec gunicorn --log-file=- \
    --worker-tmp-dir /dev/shm \
    --bind 0.0.0.0:5000 \
    --forwarded-allow-ips='*' \
    poetrybot.web.wsgi:app
