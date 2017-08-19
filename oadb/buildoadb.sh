#!/bin/bash
#
# Description: Setup the database assuming we are on a system with Python 3 in a fresh virtual environment
#

VENV_PATH=""
PYTHON_PATH=$(which python3)

while getopts "v:p:h" opt; do
  case $opt in
    v) VENV_PATH=$OPTARG ;;
    p) PYTHON_PATH=$OPTARG ;;
    h)
      echo "Usage: $0 [-v virtualenv] [-p pythonpath]"
      exit 0
      ;;
    \?)
      echo "%s: invalid argument" >&2
      exit 1
      ;;
  esac
done

if [[ -n "$VENV_PATH" ]]; then
  if [[ ! -d "$VENV_PATH" ]]; then
    virtualenv -p "$PYTHON_PATH" "$VENV_PATH"
  fi
  source "$VENV_PATH/bin/activate"
fi

pip install -r requirements.txt
rm -f db.sqlite3
./manage.py migrate
./manage.py loaddata oadb/fixtures/databases.yaml
./manage.py loaddata oadb/fixtures/systemuser.yaml
./manage.py importkits ../data/oadb_illumina_raw_dataV2.csv --username system --clear
./manage.py collectstatic --clear --noinput

