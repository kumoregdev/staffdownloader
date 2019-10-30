#!/usr/bin/env bash

if [ -f venv/bin/activate ]; then
  echo "Using virtualenv in venv/bin/activate"
  source venv/bin/activate
else
  echo "Virtualenv not found in venv directory, creating"
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi

python get_staff.py
python get_guests.py
