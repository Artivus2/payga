import datetime
import json
import re
import shutil
import sqlite3

import routers.roles.models as roles_models
import requests
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import routers.api_trader.models as trader_models
import routers.user.models as user_models
import routers.admin.models as admin_models
import config
from starlette.requests import Request

from routers.admin.controller import get_user_from_api_key, create_sms_data, get_info_for_invoice, get_pattern
from routers.admin.utils import create_access_token, get_min_amount
from routers.mains.controller import get_chart
from routers.orders.controller import create_order_for_user, insert_docs

router = APIRouter(prefix='/api/v1/trader',
                   tags=['Трейдер'],
                   dependencies=[Depends(trader_models.GetApiKey())]
                   )


@router.get("/get-api-status")
async def get_api_status():
    """
    Проверка статуса API
    :param request:
    :return:
    """
    return {"Success": True, "data": "API доступна"}


@router.get("/get-available-currencies")
async def get_charts():
    """
    https://pay.greenavi.com/api/v1/get-available-currencies
    This is a method for obtaining information about all cryptocurrencies available for payments
    for your current setup of payout and payin wallets. 0 - for all available
    :HEADERS
    x-api-key: {{api-key}}
    :(Required) Your PayGreenavi API key
    :return
    id
    symbol

    """
    response = await get_chart()
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/min-amount")
async def min_amount():
    """
    Get the minimum payment amount
    HEADERS
    x-api-key: {{api-key}}

    (Required) Your PayGreenavi API key
    :return:
    """
    response = await get_min_amount()
    return response

@router.get("/get-info-for-invoice")
async def get_info(request: Request):
    """
    req_group_id: list
    sum_fiat: float
    bank_id: int
    :param request:
    :return:
    """
    api_key = request.headers.get('x-api-key')
    response = await get_info_for_invoice(api_key)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response

#
# @router.get("/send-crypted/{uuid}")
# async def send_crypt(request: str):
#     """
#     crypt
#     """
#     payload = {}
#
#
#
# @router.post("/receive-crypted")
# async def receive_crypt(request: Request):
#     """
#     decrypt
#     """
#     reqs = await request.body()
#     string = json.loads(reqs.decode("utf-8"))
#     text = string.get('uuids')
#     to_encode = {"user_id": user_id,
#                  "role": role,
#                  "expiration": (datetime.now() + timedelta(minutes=expires_delta)).strftime("%Y-%m-%d %H:%M:%S")}
#
#     encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)



@router.post("/create-payment")
async def create_payment_for_trader(request: Request):
    """
    Creates a payment link. With this method,
    the customer is required to follow the generated url to complete the payment.

    :return:
    """
    api_key_from_merchant = request.headers.get('x-api-key')
    print(api_key_from_merchant)
    reqs = await request.body()
    string = json.loads(reqs.decode("utf-8"))
    user_id = await get_user_from_api_key(api_key_from_merchant)
    result_from_payment = {
        "req_id": string.get('req_id'),
        "sum_fiat": string.get('sum_fiat'),
        'user_id': user_id['data'],
        'pay_id': 1, # payin,
        'docs_id': string.get('docs_id', 0)
    }
    print(result_from_payment)
    response = await create_order_for_user(result_from_payment)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/create-payout")
async def create_payout_for_trader(request: Request):
    """
    Creates a payout for trader. With this method,
    the customer is required to withdrawals funds.

    :return:
    """
    api_key_from_merchant = request.headers.get('x-api-key')
    print(api_key_from_merchant)
    reqs = await request.body()
    string = json.loads(reqs.decode("utf-8"))
    user_id = await get_user_from_api_key(api_key_from_merchant)
    result_from_payout = {
        "req_id": string.get('req_id'),
        "sum_fiat": string.get('sum_fiat'),
        'phone': string.get('phone'),
        'user_id': user_id['data'],
        'pay_id': 2,  # payout
    }
    print(result_from_payout)
    response = await create_order_for_user(result_from_payout)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/sms-data")
async def sms_receiver(request: Request):
    """
    SMS Receiver
    :param request:
    :param id:
    :return:
    """
    reqs = await request.body()
    string = json.loads(reqs.decode("utf-8"))
    text = string.get('text',0)
    sender = string.get('smsFrom',0)
    api_key_from_merchant = request.headers.get('x-api-key', 0)
    user_id = await get_user_from_api_key(api_key_from_merchant)
    if user_id['Success']:
        result = await get_pattern(sender, text)
        if result['Success']:
            result["user_id"] = user_id['data']
            response = await create_sms_data(result)
            if not response['Success']:
                raise HTTPException(
                    status_code=400,
                    detail="Операция не выполнена, " + str(response['data'])
                )
            return response
        else:
            #перевести в статус 4 ? не знаем № ордера
            raise HTTPException(
                status_code=400,
                detail="Автоматизация не проведена. пропускаем ордер"
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не найден"
        )