#!/bin/bash

python3 /home/supervisor/solar-data-receiver/driver.py >> /home/supervisor/solar-data-receiver/logs/mqtt_solar_receive-`date '+%Y%m%d'`.log 2>&1
