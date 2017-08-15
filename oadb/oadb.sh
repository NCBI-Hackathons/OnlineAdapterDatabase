#!/bin/bash
gunicorn -w 4 oadb.wsgi
