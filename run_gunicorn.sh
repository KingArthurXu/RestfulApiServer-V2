#!/usr/bin/env bash

gunicorn -c gunicorn_frun.py frun:app

gunicorn -w 4 -b 0.0.0.0:5000 --log-level debug --daemon frun:app --access-logfile '-'

gunicorn -w 4 -b 0.0.0.0:5000 frun:app

gunicorn -w 1 -b 0.0.0.0:5001 --log-level debug brun:app --access-logfile -

pip freeze > requirements.txt

uwsgi --socket 0.0.0.0:5000 --wsgi-file frun.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:9191

