FROM ubuntu:16.04

LABEL oadb.version=0.2

RUN apt-get update && apt-get -y upgrade && apt-get -y install cron python python3
RUN apt-get install -y python3-pip build-essential python-virtualenv

COPY oadb /opt/oadb/oadb/
COPY data /opt/oadb/data/

WORKDIR /opt/oadb/oadb
RUN virtualenv /opt/oadb/oadb/venv -p /usr/bin/python3
RUN cd /opt/oadb/oadb
RUN source /opt/oadb/venv/bin/activate
RUN ./buildoadb.sh
