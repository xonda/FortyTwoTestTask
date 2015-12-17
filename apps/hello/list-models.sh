#!/bin/bash

DATE=`date +%d-%m-%Y`
source /home/derp/code/42/env/bin/activate
python /home/derp/code/42/42test/manage.py list_models 2>> /home/derp/code/42/42test/apps/hello/$DATE.dat