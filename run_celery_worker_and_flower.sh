#!/bin/bash
# By executing this script you will run celery worker for email sending
# Mandatory arguments must be given when running this script
# 1. Email to be used as sender email
# 2. Password of sender email 
# This script only runs in Linux or Mac
if [ "$#" != 2 ]
then
    echo "Usage: ./run_celery_worker.sh <email> <password>"
    exit 0
fi
MAIL_USERNAME="$1"
export MAIL_USERNAME
MAIL_PASSWORD="$2"
export MAIL_PASSWORD
DATABASE_URI=sqlite:////tmp/jublia_email_autosend.db
export DATABASE_URI
celery flower -A jublia_email_autosend.celery_app:app --address=127.0.0.1 --port=5555 &
celery worker -A jublia_email_autosend.celery_app:app --loglevel=info