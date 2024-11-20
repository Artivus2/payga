import re
import json
import routers.user.models as user_models
import requests
from fastapi import APIRouter, HTTPException
from routers.user.utils import hash_from_yii2
from routers.user.controller import insert_new_user_banned, insert_generated_api_key, get_token_by_user_id

import config

router = APIRouter(prefix='/api/v1/user', tags=['User'])


@router.get("/get-jwt-token/{token}")
async def get_jwt_token(token: str):
    """
    Запрос токена
    :param request:
    :return:
    token
    """
    return await get_token_by_user_id(token)


@router.post("/login")
async def login(request: user_models.Login):
    """
    email
    password
    :return:
    {token}
    """
    api_url = f'{config.BASE_URL}/api/user/login'
    headers = {
        'Content-Type': 'application/json',

    }
    payload = {
        'email': request.email,  # req
        'password': request.password  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    print(response)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/code")
async def code(request: user_models.Code):
    """
    запрос токена авторизации
    :param request: email, password, code
    :return:
    {access_token}
    """
    api_url = f'{config.BASE_URL}/api/user/code'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': request.email,  # req
        'password': request.password,  # req
        'code': request.code  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    print(response.json())
    return response.json()


@router.post("/logout")
async def logout(request: user_models.Logout):
    """
    Логаут
    :param request:
    token
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/logout'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'token': request.token
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/register-request")
async def register_request(request: user_models.User):
    """
    login: Логин,
    email: емаил,
    telegram: телеграм
    affiliate_invitation_id: реф,
    password: пароль,
    :param request:
    :return:
    {comment возращает ссылку на регистрацию после подтверждения администратора, отправляет на почту пользователю}
    """
    hashed_password = await hash_from_yii2(request.password)
    payload = {
        'email': request.email,
        'login': request.login,
        'telegram': request.telegram,
        'affiliate_invitation_id': request.affiliate_invitation_id,
        'password': hashed_password['password']
    }
    pattern = '/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/' #todo
    if not payload['login'] or not payload['email'] or not payload['telegram'] or not payload['password']:
        #or len(re.findall(pattern, payload['email'])) > 0:
        return {"status": False, "message": "Указаны не все обязательные параметры при отправке заявки на регистрацию!"}
    return await insert_new_user_banned(**payload)

@router.post("/two-factor-new")
async def two_factor_new(request: user_models.Twofa):
    """
    token: str
    user_id: int
    :param request:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/two-factor-new'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': request.token # везде
    }
    payload = {
        'user_id': request.user_id,
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/two-factor")
async def two_factor(request: user_models.Twofa):
    """
    token: str
    user_id: int
    :param request:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/two-factor'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': request.token
    }
    payload = {
        'user_id': request.user_id,
        'secret': request.secret
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/two-factor-disable")
async def disable_2fa(request: user_models.Twofa):
    """
    token: str
    user_id: int
    :param request:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/two-factor-disable'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': request.token,
    }
    payload = {
        'user_id': request.user_id,
        'secret': request.secret
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/change-password")
async def change_password(request: user_models.User):
    pass

@router.post("/generate-user-apikey")
async def generate_user_apikey(request: user_models.ApiKey):
    return await insert_generated_api_key(request.user_id)

@router.post("/remove-user-apikey")
async def remove_user_apikey(request: user_models.User):
    pass
