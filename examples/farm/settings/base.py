import os

import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from aiobots.helpers import generate_secret_key


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')


APPS_REGISTRY = (
    'mybot',
)

HOSTNAME = 'localhost'
PORT = '8000'

SECRET_KEY = generate_secret_key()

SESSION_STORAGE = EncryptedCookieStorage(SECRET_KEY)
