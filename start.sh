#!/usr/bin/env bash


cd /root/course_work
source .venv/bin/activate

# НАЗВАНИЕ_ФАЙЛА:НАЗВАНИЕ_ОБЪЕТА_FLASK
gunicorn app:app -b :5000
