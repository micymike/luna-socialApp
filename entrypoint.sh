#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
flask db upgrade

# Start the Flask application
exec gunicorn -b :8080 --access-logfile - --error-logfile - app:app
