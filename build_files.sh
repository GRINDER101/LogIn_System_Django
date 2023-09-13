#!/bin/bash

# Build the project
echo "Building the project..."
python2.7 -m pip install -r requirements.txt

echo "Make Migration..."
python2.7 manage.py makemigrations --noinput
python2.7 manage.py migrate --noinput

echo "Collect Static..."
python2.7 manage.py collectstatic --noinput --clear