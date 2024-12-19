#!/user/bin/env bash
exec gunicorn -b :5000 --workers 1 --threads 8 --timeout 0 app:app