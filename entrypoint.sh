#!/bin/bash
set -e

# Default: RunPod serverless mode
# For local testing: docker run with LOCAL_TEST=1
if [ "${LOCAL_TEST:-0}" = "1" ]; then
    echo "Starting in LOCAL TEST mode..."
    exec python /app/src/handler.py --rp_serve_api --rp_api_host 0.0.0.0 --rp_api_port 8000
else
    echo "Starting in RUNPOD SERVERLESS mode..."
    exec python /app/src/handler.py
fi
