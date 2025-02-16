import datetime
import re
import json
from typing import Annotated

import qrcode

import config
import routers.user.models as user_models
import requests
import telebot
from fastapi import APIRouter, HTTPException, Cookie, Request, Response
from routers.admin.controller import insert_new_user_banned
from routers.admin.utils import get_hash, verify, create_access_token, send_mail
from routers.user.controller import (
    insert_generated_api_key,
    get_user_api_key,
    delete_user_api_key_by_id,
    get_profile_by_id,
    get_user_by_email,
    set_user_active_token,
    set_user_active_onoff,
    send_code,
    check_code,
    set_two_fa_status,
    get_two_fa_digits,
    get_two_fa_key

)
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
botgreenavipay = telebot.TeleBot(config.telegram_api)
router = APIRouter(prefix='/api/v1/user', include_in_schema=False, tags=['Пользователи'])


# @router.get("/jwt-token/{token}")
# async def get_jwt_token(token: str):
#     """
#     Запрос токена
#     :param token:
#     :return:
#     token
#     """
#     print(token)
#     response = await get_token_by_token(token)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     return response


# @router.post("/get-refresh-token")
# async def refresh_token(token: str):
#     #todo
#     """
#     рефреш токена
#     :param token:
#     :return:
#     token
#     """
#     response = await get_refresh_token(token)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response.json(),
#         )
#     return response.json()


# @router.post("/get-refresh-token") # todo
# async def refresh(user_id: int):
#     print(user_id)
#     response = await check_user_by_id(user_id)
#     if not response['Success']:
#         raise BadRequestException(detail="refresh token required")
#     print(create_token_pair(user_id))
#     return create_token_pair(user_id)


@router.post("/logout")
async def logout(request: Request):
    """
    Логаут
    :param request:
    token
    :return:
    """
    print(request.headers.get('authorization'))




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



@router.post("/register-request")
async def register_request(request: user_models.User):
    """
    login: Логин,
    email: емаил,
    telegram: телеграм
    affiliate_invitation_code: реф,
    password: пароль,
    :param request:
    :return:
    {comment возращает ссылку на регистрацию после подтверждения администратора, отправляет на почту пользователю}
    """
    hashed_password = await get_hash(request.password)

    payload = {
        'email': request.email,
        'login': request.login,
        'telegram': request.telegram,
        'affiliate_invitation_code': request.affiliate_invitation_code,
        'password': hashed_password
    }


    if not payload['login'] or not payload['email'] or not payload['telegram'] or not payload['password']:
        # or len(re.findall(pattern, payload['email'])) > 0:
        return {"status": False, "message": "Указаны не все обязательные параметры при отправке заявки на регистрацию!"}
    response = await insert_new_user_banned(**payload)

    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.post("/code")
async def code(request: user_models.Login):
    """
    запрос токена авторизации
    :param request: email, password, code
    :return:
    {access_token}
    """
    user = await get_user_by_email(request.email)
    if not user['Success']:
        raise HTTPException(status_code=404,
                            detail=f"Указаны не верные данные !")

    if not await verify(request.password, user['data']['password']):
        raise HTTPException(status_code=404,
                            detail=f"Пароль указан неверно !")

    response = await check_code(request.code, user['data']['id'])
    # if response.code != '111111':
    #     raise HTTPException(status_code=401, detail="Не верный код авторизации")
    if response['Success']:
        access_token = create_access_token(user_id=user['data']['email'],
                                           role=user['data']['role_id'],
                                           expires_delta=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        #
        # Change the active status of the user -->True(1)
        itog = await set_user_active_token(user['data']['email'], datetime.datetime.utcnow(), access_token)
        if not itog['Success']:
            raise HTTPException(status_code=404,
                                detail=f"Не удалось получить токен")
        await send_mail("Пользователь "+str(user['data']['login'])+ " авторизирован", "Успешная авторизация", user['data']['email'])
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "data": {
                "id": user['data']['id'],
                "email": user['data']['email'],
                "login": user['data']['login'],
                "role_id": user['data']['role_id']
            }
        }
    else:
        raise HTTPException(status_code=404,
                            detail=f"Указан не верный код подтверждения!")


@router.post('/login')
async def login_for_access_token(request: user_models.Login):
    ## To see if username/email exsist in Database
    user = await get_user_by_email(request.email)
    if not user['Success']:
        raise HTTPException(status_code=404,
                            detail=f"Указаны не верные данные !")

    if not await verify(request.password, user['data']['password']):
        raise HTTPException(status_code=404,
                            detail=f"Пароль указан неверно !")

    ##отпрваили код на почту
    result = await send_code(user['data']['id'])
    if result["Success"]:
        return result["data"]
    else:
        raise HTTPException(status_code=404,
                            detail=f"Не удалось получить токен")




# @router.post('/login-with-2fa')
# async def login_for_access_token_with_otp(request: user_models.LoginOTP):
#     print(request)
#     ## To see if username/email exsist in Database
#     user = await get_user_by_email(request.email)
#
#     print(user['data']['password'])
#     if not user['Success']:
#         raise HTTPException(status_code=404,
#                             detail=f"Invalid Creadentials. !")
#
#     if not await verify(request.password, user['data']['otp']):
#         raise HTTPException(status_code=404,
#                             detail=f"Incorrect OTP. !")
#
#     ## Generate and return JWT token
#     access_token = create_access_token(subject=user['data']['email'],
#                                        expires_delta=config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     #
#     # Change the active status of the user -->True(1)
#     await set_user_active(user['data']['email'], datetime.datetime.utcnow())
#
#
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "data": {
#             "id": user['data']['id'],
#             "email": user['data']['email'],
#             "login": user['data']['login']
#         }
#     }

@router.put("/change-password")
async def change_password(request: user_models.User):
    """
    Смена пароля
    :param request:
    :return:
    """
    api_url = f'{config.BASE_URL}/api/user/change-password'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': request.token,
    }
    payload = {
        'email': request.email,
        'password': request.password
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/confirm-password")
async def change_password(request: user_models.User):
    pass


@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    """
    Запрос профиля
    :param user_id:
    :return:
    token
    """
    response = await get_profile_by_id(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response



@router.post("/generate-user-apikey")
async def generate_user_apikey(request: user_models.ApiKey):
    """
    образец по user_id{}
    :param request:
    :return:
    response
    """
    response = await insert_generated_api_key(request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.get("/get-user-apikey/{user_id}")
async def get_user_apikey(user_id: int):
    """
    образец по user_id{}
    :param user_id:
    :return:
    response
    """
    response = await get_user_api_key(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )

    return response



@router.post("/set-active")
async def set_user_onoff(request: user_models.User):
    """
    образец по user_id{}
    :param request:
    :param user_id:
    :return:
    response
    """
    response = await set_user_active_onoff(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )

    return response



@router.get("/profile-app")
async def read_profile(request: Request):

    """
    Запрос профиля
    :param token:
    :param user_id:
    :return:
    token
    """
    # response = await get_profile_by_id(request.id)
    # if not response['Success']:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=response
    #     )
    print(request.headers.get('authorization'))
    return {"success":True}






@router.delete("/delete-user-apikey")
async def delete_user_apikey(request: user_models.ApiKey):
    """
    образец по id
    :param request:
    :return:
    response
    """
    response = await delete_user_api_key_by_id(request.id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response



@router.post("/control-2fa")
async def e2fa(request: user_models.User):
    """
    включить 2fa
    """
    data = await set_two_fa_status(request)
    return data


@router.post("/check-2fa")
async def g2fa(request: user_models.User):
    """
    получить цифры 2fa
    """
    result = await get_two_fa_digits(request)
    return result



@router.get("/get-key-2fa/{user_id}")
async def c2fa(user_id: int):
    """
    получить ключ 2fa
    """
    result = await get_two_fa_key(user_id)
    return result