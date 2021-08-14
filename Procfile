web: gunicorn --bind 127.0.0.1:8000 --workers=1 --threads=15 fitweb.wsgi:application
websocket: daphne -b 0.0.0.0 -p 5000 fitweb.asgi:application
