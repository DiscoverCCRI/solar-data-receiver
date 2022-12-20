#!/bin/bash

python3 /home/supervisor/solar-data-receive/driver.py >> /home/supervisor/solar-data-receive/logs/mqtt-solar-receive-`date '+%Y%m%d'`.log 2>&1
