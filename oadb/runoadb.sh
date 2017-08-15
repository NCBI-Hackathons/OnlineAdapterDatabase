#!/bin/bash
BINDADDR="*.*.*.*"
BINDPORT=8001

while getopts "a:p:" opt; do
  case $opt in
    a) BINDADDR=$PTARG ;;
    p) BINDPORT=$OPTARG ;;
    \?) echo "error: invalid argument" >&2; exit 1 ;;
  esac
done

shift $((OPTIND-1))

gunicorn -w 4 oadb.wsgi "$BINDADDR:$BINDPORT"
