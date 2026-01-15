#!/bin/bash
# Start script for Render.com deployment

PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

uvicorn api.main:app \
  --host $HOST \
  --port $PORT \
  --workers 1
