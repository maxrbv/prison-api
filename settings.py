from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / 'web' / 'templates'
STATIC_DIR = BASE_DIR / 'web' / 'static'

DB_URL = 'postgres://postgres:postgres@localhost:5432/ton_prison'
TOKEN = '6985109097:AAFML8yVtiwXnapbV8AHl7qxXgJIMwsQxWY'
WEBAPP_URL = 'https://27d5-94-50-241-216.ngrok-free.app'
