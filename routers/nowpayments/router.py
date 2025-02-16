import json
from hashlib import sha256
import requests
from fastapi import APIRouter, HTTPException, Header
import config
from routers.nowpayments import models
from routers.nowpayments.controller import (
    get_jwt_token
    )

router = APIRouter(prefix='/np', include_in_schema=False, tags=['NowPayments'])


# List currencies
@router.get("/list_currencies")
def list_currencies():
    api_url = f'{config.base_url_np}currencies'
    headers = {
        'x-api-key': config.api_key_np,
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


# Create payment
@router.post("/create_payment")
async def create_payment(request: models.CreatePaymentRequest):
    url = f"{config.base_url_np}payment"
    headers = {
        "x-api-key": config.api_key_np,
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
@router.post("/create_payout")
def create_payout(request: models.CreatePayoutRequest):
    jwt_token = get_jwt_token()
    url = f"{config.base_url_np}payout"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'x-api-key': config.api_key_np,
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


# Get payment status
@router.get("/get_payment_status/{payment_id}")
def get_payment_status(payment_id: str):
    url = f"{config.base_url_np}payment/{payment_id}"
    headers = {
        "x-api-key": config.api_key_np,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    print(response.json())
    return response.json()



#get_payout_status
@router.get("/get_payout_status/{payout_id}")
def get_payment_status(payout_id: str):
    url = f"{config.base_url_np}payout/{payout_id}"
    headers = {
        "x-api-key": config.api_key_np,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()




@router.get("/get_payout_fee/{amount}")
def get_payment_status(amount: str):
    url = f"{config.base_url_np}payout/fee?currency=USDTTRC20&amount={amount}"
    headers = {
        "x-api-key": config.api_key_np,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()



@router.get("/fp/wallet/history")
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
        "apikey": config.BSC_API_KEY
    }

    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    transactions = response.json().get("result", [])

    # Modify transaction ID to hash
    for transaction in transactions:
        transaction['hash'] = sha256(transaction['hash'].encode()).hexdigest()
    return transactions


@router.post("/get_jwt_token")
def get_jwt_token_endpoint(request: models.JwtRequest):
    return get_jwt_token()




@router.post("/verify-payout")
async def verify_payout_id(request: models.VerifyPayout):
    """
    id payout merchant verify
    """
    if not request.code:
        raise HTTPException(status_code=400, detail="Для вывода включите 2ФА верификацию")
    jwt_token = get_jwt_token()
    url = f"{config.base_url_np}{str(request.payout_id)}/verify"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'x-api-key': config.api_key_np,
        'Content-Type': 'application/json'
    }
    payload = {
        'verification_code': request.code
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()