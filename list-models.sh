#!/bin/bash

DATE=`date +%d-%m-%Y`
python /home/derp/code/42/42test/manage.py list_models 2>> $DATE.dat