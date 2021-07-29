web: gunicorn --bind :8000 --workers 3 --threads 2 fitweb.wsgi:application
websocket: daphne -b :: -p 5000 fitweb.asgi:channel_layers