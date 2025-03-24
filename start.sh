#!/bin/bash
# Update package lists
apt-get update

# Install Tesseract OCR
apt-get install -y tesseract-ocr

# Start the Flask app with Gunicorn
gunicorn app:app --bind 0.0.0.0:5000
