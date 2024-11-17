import asyncio
import uvicorn
import models.models
import requests
import json
from fastapi import FastAPI, HTTPException, Depends, Header, Query


app = FastAPI()

@app.get("/")
async def route():
    return "root"

@app.get("/api/v1/test")
async def test():
    return "all ok"

@app.get("/jwt")
def get_jwt_token(request: models.models.JwtRequest):
    email = 'artivus3@yandex.ru'
    password = 'Adm142!@'
    base_url = 'https://greenavi.com'
    api_url = f'{base_url}/api/user/login'
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # payload = {
    #     'email': email, #req
    #     'password': password #req
    # }
    # response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code, detail=response.json())
    # print(response.json())
    #return response.json()
    return api_url

async def main():
    config = uvicorn.Config("main:app", port=5001, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
