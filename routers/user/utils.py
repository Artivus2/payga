import json
import secrets
import string
import requests
from fastapi import HTTPException
import config


async def hash_from_yii2(password):
    """
    получить хешкод пароля из yii2
    :param password:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/get-password'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'password': password  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


async def create_random_key(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(secrets.choice(chars) for _ in range(length))