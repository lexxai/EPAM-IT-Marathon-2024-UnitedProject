#!/bin/sh

#python3 -m venv .env
echo "Run run.sh"
pwd
pip install --no-cache-dir --upgrade -r requirements.txt
cd pet-project || exit
pwd
# alembic upgrade head
run "gunicorn"
gunicorn main:main_app