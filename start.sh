#!/bin/bash

# Ensure pip is updated
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Start the app using Gunicorn
gunicorn app:app --bind 0.0.0.0:5000
