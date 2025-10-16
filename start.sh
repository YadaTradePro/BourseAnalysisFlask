#!/bin/bash
# YadaTradeBackend Startup Script

echo "=== YadaTradeBackend Starting ==="
echo "Environment: $(uname -a)"
echo "Python version: $(python --version)"
echo ""

# Start the Flask application using gunicorn
echo "Starting Flask API with Gunicorn..."
exec gunicorn --workers 2 --worker-class gevent --bind 0.0.0.0:5000 --timeout 0 "main:create_app()"
