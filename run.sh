#!/bin/bash

cd /home/last/programming/envs/mailru_first/hello
source ../bin/activate
exec ../bin/gunicorn hello.wsgi:application --bind unix:./run/gunicorn.sock --workers 9 --name mytasktracker

