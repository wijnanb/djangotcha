#!/bin/bash
ROOT="/home/ubuntu/git/djangotcha"

cd $ROOT
. /home/ubuntu/.virtualenvs/djangotcha/bin/activate
exec /home/ubuntu/.virtualenvs/djangotcha/bin/python manage.py run_gunicorn -b 0.0.0.0:8001 \
    --log-file=/var/log/djangotcha.log


