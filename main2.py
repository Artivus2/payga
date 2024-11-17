from fastapi import FastAPI, HTTPException, Depends, Header, Query
from pydantic import BaseModel
import requests
import json
from fastapi.responses import RedirectResponse
from hashlib import sha256
import models.models

app = FastAPI()
email = 'test.greenavi@mail.ru'  # Replace with your NowPayments email
password = 'M354at790!'  # Replace with your NowPayments password
base_url = 'https://api.nowpayments.io/v1/'

# Models

def get_jwt_token():
    api_url = 'https://api.nowpayments.io/v1/auth'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    print(response.json()["token"])
    return response.json()["token"]


# List currencies
@app.get("/list_currencies")
def list_currencies():
    api_url = f'{base_url}currencies'
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


# Create payment
@app.post("/create_payment")
def create_payment(request: models.CreatePaymentRequest):
    url = f"{base_url}payment"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "price_amount": request.amount,
        "price_currency": request.currency,
        "order_id": request.order_id,
        "pay_currency": request.pay_currency
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


# Create payout
@app.post("/create_payout")
def create_payout(request: CreatePayoutRequest):
    jwt_token = get_jwt_token()
    url = f"{base_url}payout"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'withdrawals': [
            {
                'address': request.address,
                'amount': request.amount,
                'currency': request.currency,
                'ipn_callback_url': 'https://greenavi.com/api/payment/notice-ipn'  # Your IPN callback URL
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@app.post("/get_jwt_token")
def get_jwt_token_endpoint(request: JwtRequest):
    return get_jwt_token()


# Get JWT token
# @app.post("/get_jwt_token")
# def get_jwt_token(request: JwtRequest):
#     api_url = f'{base_url}auth'
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     payload = {
#         'email': request.email,
#         'password': request.password
#     }
#     response = requests.post(api_url, headers=headers, data=json.dumps(payload))
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail=response.json())
#     return response.json()

# Get payment status
@app.get("/get_payment_status/{payment_id}")
def get_payment_status(payment_id: str):
    url = f"{base_url}payment/{payment_id}"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@app.get("/fp/wallet/history")
def get_wallet_history(
        address: str,
        page: int,
        offset: int,
        authorization: str = Header(...)
):
    # Extract the token from the authorization header
    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header is empty (Bearer JWT token is required)")

    # BscScan API URL
    api_url = f"https://api.bscscan.com/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": page,
        "offset": offset,
        "sort": "asc",
        "apikey": BSC_API_KEY
    }

    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    transactions = response.json().get("result", [])

    # Modify transaction ID to hash
    for transaction in transactions:
        transaction['hash'] = sha256(transaction['hash'].encode()).hexdigest()

    return transactions