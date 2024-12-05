from fastapi import FastAPI, HTTPException, Depends, Header, Query
import requests
import json
from routers.nowpayments import models


def get_jwt_token():
    api_url = 'https://api.nowpayments.io/v1/auth'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': models.JwtRequest.email,
        'password': models.JwtRequest.password
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    #print(response.json()["token"])
    return response.json()["token"]




