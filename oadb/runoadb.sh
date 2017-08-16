#!/bin/bash

BINDADDR="0.0.0.0"
BINDPORT=8001
SETTINGS=oadb.settings.dev

while getopts "a:p:s:h" opt; do
  case $opt in
    h) 
      echo "Usage: $0 [options]" ;
      echo "   -h ...... help (this message)" ;
      echo "   -a ...... bind address, defaults to 0.0.0.0 for all interfaces" ;
      echo "   -p ...... bind port, defaults to 8001 to avoid conflict with runserver" ;
      echo "   -s ...... Django settings module - this doesn't work yet" ;
      exit 0 ;;
    a) BINDADDR=$OPTARG ;;
    p) BINDPORT=$OPTARG ;;
    s) SETTINGS=$OPTARG ;;
    \?) echo "error: invalid argument - use -h for usage" >&2; exit 1 ;;
  esac
done

shift $((OPTIND-1))

echo "Starting web interface - go to http://localhost:$BINDPORT/"

export DJANGO_SETTINGS_MODULE="$SETTINGS"
gunicorn -w 4 oadb.wsgi -b "$BINDADDR:$BINDPORT"
