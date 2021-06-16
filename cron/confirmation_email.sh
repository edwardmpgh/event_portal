#!/usr/bin/env bash

# This script sends the confirmation email to attendees
# Set it up to run with cron

# start the Python virtual environment
. /home/heinz/env/heinz_signup/bin/activate

# runt he script
cd /home/heinz/pyprojects/heinz_signup
python3 manage.py send_confirmation_email
deactivate