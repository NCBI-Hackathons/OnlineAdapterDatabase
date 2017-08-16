# AWS-based Demo

## Background

During the NCBI-hackathon, each team is issued an AWS EC2 instance to host their software, 
and make sure they have access to common tools.  Our instructions are to ssh into this instance
with a local port mapping, like this:

    ssh -L 7777:localhost:80 ubuntu@a.c.b.d

All well and good, but Linux doesn't let us to use port 80 as root, and the NIH Wireless Guest 
network will not permit a connection directly to http://a.b.c.d/.   Theoretically, it will work
if the firewalls allow it - but we could not reach http://a.b.c.d/ on our cell phones either.
Maybe this is possible if you connect to the NIH Wireless network *FOR STAFF ONLY*.

## Solutions

Three solutions present themselves:

 - run the Django/gunicorn server as root on port 80
 - Use a web server on port 80 and proxy to the Django/gunicorn on a non-restricted port (default 8000)
 - Change the local forward to use a different port to ubuntu

The simplest for our demo is to run the Django/gunicorn server as root on port 80.

## Procedure

- Enter the virtualenv

      . ~/venv/bin/activate

- Refresh the repository with git pull

      cd oadb-active/OnlineAdapterDatabase
      git pull

- Make sure the data and packages are up to date

      cd oadb
      ./oadbbuild.sh

- Become root and get back where you were:

    # Become root
    sudo su - 

    # Activate the virtualenv
    . ~ubuntu/venv/bin/activate

    # Go to the Django project directory
    cd ~ubuntu/oadb-active/OnlineAdapterDatabase/oadb

- Start the server on port 80

    ./runoadb.sh -p 80


