#!/bin/bash
#
# Description: Setup the database assuming we are on a system with Python 3 in a fresh virtual environment
#
pip install -r requirements.txt
rm -f db.sqlite3
./manage.py migrate
./manage.py loaddata oadb/fixtures/databases.yaml
./manage.py loaddata oadb/fixtures/systemuser.yaml
./manage.py importkits ../data/oadb_illumina_raw_dataV2.csv --username system --clear
./manage.py importkits ../data/old_adapters.csv --username system --format chaim
./manage.py loaddata oadb/fixtures/dummyrun.yaml
./manage.py collectstatic --clear --noinput

