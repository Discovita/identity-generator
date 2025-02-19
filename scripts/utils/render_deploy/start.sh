#!/bin/bash
set -e

cd backend
. .venv/bin/activate
exec uvicorn discovita.app:app --host 0.0.0.0 --port $PORT
