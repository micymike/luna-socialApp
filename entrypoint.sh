#!/bin/sh

# Run database migrations
flask db upgrade

# Start the Flask application
exec gunicorn -b :8080 --access-logfile - --error-logfile - app:app
