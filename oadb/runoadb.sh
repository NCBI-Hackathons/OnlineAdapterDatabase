#!/bin/bash

BINDADDR="0.0.0.0"
BINDPORT=8000
SETTINGS=oadb.settings.standalone
VENV_PATH=""

while getopts "a:p:s:v:h" opt; do
  case $opt in
    h) 
      echo "Usage: $0 [options]"
      echo "   -h ........... help (this message)"
      echo "   -a ADDRESS ... bind address, defaults to 0.0.0.0 for all interfaces"
      echo "   -p PORT ...... bind port, defaults to 8001 to avoid conflict with runserver"
      echo "   -v PATH ...... path to virtual environment to activate"
      echo "   -s ...... Django settings module - this doesn't work yet"
      exit 0 ;;
    a) BINDADDR=$OPTARG ;;
    p) BINDPORT=$OPTARG ;;
    s) SETTINGS=$OPTARG ;;
    v) VENV_PATH=$OPTARG ;;
    \?) echo "error: invalid argument - use -h for usage" >&2; exit 1 ;;
  esac
done

shift $((OPTIND-1))

if [[ -n $VENV_PATH ]]; then
  if [[ ! -f "$VENV_PATH/bin/activate" ]]; then
    echo "$VENV_PATH: not a python virtualenv" >&2
    exit 1
  fi
  source "$VENV_PATH/bin/activate"
fi

export DJANGO_SETTINGS_MODULE="$SETTINGS"
gunicorn -w 4 oadb.wsgi -b "$BINDADDR:$BINDPORT"

