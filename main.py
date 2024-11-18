import asyncio
import mysql.connector.aio as cpy_async
import uvicorn
import models.models
import requests
import json
from fastapi import FastAPI, HTTPException, Depends, Header, Query
import mysql


base_url = 'http://localhost'
app = FastAPI()


@app.get("/")
async def route():
    return "root"


@app.get("/api/v1/test")
async def api1():
    config = {
        'user': 'greenavi_user',
        'password': 'tb7x3Er5PQ',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'greenavi_app',
        'raise_on_warnings': True
    }
    #cnx = mysql.connector.connect(**config)
    async with await cpy_async.connect(**config) as cnx:
        async with await cnx.cursor() as cur:
            await cur.execute("SELECT @@version")
            print(await cur.fetchall())

@app.post("/api/v1/user/logout")
async def logout(request: models.models.Logout):
    """
    Логаут
    :param request:
    token
    :return:
    """
    api_url = f'{base_url}/api/user/logout'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'token': request.token,  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@app.post("/api/v1/user/register-request")
async def register_request(request: models.models.RegisterRequest):
    """
    login: Логин,
    email: емаил,
    telegram: телеграм
    affiliate: реф,
    password: пароль,
    :param request:
    :return:
    {comment возращает ссылку на регистрацию после подтверждения администратора, отправляет на почту пользователю}
    """
    hashed_password = await hashFromYii2(request.password)
    #hashed_password = '1212'
    payload = {
        'email': request.email,  # req
        'login': request.login,  # req
        'telegram': request.telegram,  # req
        'affiliate': request.affiliate,  # req
        'password': hashed_password['password'],  # req
    }
    print(payload)
    models.models.insert_new_user(**payload)




async def hashFromYii2(password):
    """
    получить хешкод пароля из yii2
    :param password:
    :return:
    """
    api_url = f'{base_url}/api/user/get-password'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'password': password  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    print(response.json())
    return response.json()


@app.post("/api/v1/user/login")
async def login(request: models.models.Login):
    """
    email
    password
    :return:
    {token}
    """
    api_url = f'{base_url}/api/user/login'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': request.email,  # req
        'password': request.password  # req
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@app.post("/api/v1/user/code")
async def code(request: models.models.Code):
    """
    запрос токена авторизации
    :param request: email, password, code
    :return:
    {access_token}
    """
    api_url = f'{base_url}/api/user/code'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': request.email,  # req
        'password': request.password,  # req
        'code': request.code  # req
    }
    print(payload)
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    print(response.json())
    return response.json()


async def main():
    config = uvicorn.Config("main:app", port=5001, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
