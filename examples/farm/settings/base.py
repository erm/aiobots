import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')


APPS_REGISTRY = (
    'markov',
)

HOSTNAME = 'localhost'
PORT = '8000'
