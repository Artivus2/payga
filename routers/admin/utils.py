import json
from fastapi import HTTPException
import config
import requests

async def send_email_yii2(login, email):
    """
    отправить почту пользователю
    :param login, email:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/send-email'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'login': login,
        'email': email
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()