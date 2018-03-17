import base64
import os

from aiohttp_session import get_session
from passlib.hash import sha256_crypt


def generate_session_id(num_bytes=16):
    return base64.b64encode(os.urandom(num_bytes))


async def get_identity(session):
    identity = session.get('AIOBOTS_IDENTITY')
    if not identity:
        session_id = generate_session_id()
        identity = {
            '__id__': session_id.decode('utf-8').replace("'", '"'),
        }
        session['AIOBOTS_IDENTITY'] = identity
    return identity['__id__']
