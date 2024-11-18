import asyncio
import uvicorn
import models.models
import requests
import json
from fastapi import FastAPI, HTTPException, Depends, Header, Query

base_url = 'https://greenavi.com'
app = FastAPI()


@app.get("/")
async def route():
    return "root"


@app.get("/api/v1/test")
async def api1():
    return "all ok"


@app.get("/api/v1/login")
async def login(request: models.models.Login):
    '''
    email
    password
    :return:
    {код} 
    '''
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


@app.post("/jwt")
async def get_jwt_token(request: models.models.JwtRequest):
    '''
    запрос токена авторизации
    :param request: email, password
    :return: 
    token
    base_url = 'https://greenavi.com'
    api_url = f'{base_url}/api/user/send-code'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': request.email, #req
        'password': request.password #req
    }
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
