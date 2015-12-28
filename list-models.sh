#!/bin/bash

DATE=`date +%d-%m-%Y`
python manage.py list_models 2>> $DATE.dat