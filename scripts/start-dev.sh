#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Start Django dev server
echo "Starting Django dev server on 0.0.0.0:8000"
python3 manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Start ngrok
echo "Starting ngrok on port 8000"
ngrok http 8000 --log=stdout > ngrok.log 2>&1 &
NGROK_PID=$!

# Wait a bit for ngrok to be available
sleep 2
curl -s http://127.0.0.1:4040/api/tunnels || true

trap "echo 'Stopping processes'; kill $DJANGO_PID $NGROK_PID; exit" SIGINT SIGTERM

echo "Tailing ngrok.log (press Ctrl-C to stop)"
tail -f ngrok.log
