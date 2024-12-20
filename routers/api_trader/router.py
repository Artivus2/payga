import datetime
import json
import re
import sqlite3

import routers.roles.models as roles_models
import requests
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import routers.api_trader.models as trader_models
import routers.user.models as user_models
import routers.admin.models as admin_models
import config
from starlette.requests import Request

from routers.admin.controller import get_user_from_api_key, create_sms_data
from routers.admin.utils import create_access_token, get_min_amount
from routers.mains.controller import get_chart
from routers.orders.controller import create_order_for_user

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
        'pay_id': 1 # payin
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
    result_from_invoice = {
        "req_id": string.get('req_id'),
        "sum_fiat": string.get('sum_fiat'),
        'phone': string.get('phone'),
        'user_id': user_id['data'],
        'pay_id': 2,  # payout


    }
    print(result_from_invoice)
    response = await create_order_for_user(result_from_invoice)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response

# @router.post("/sms-data")
# async def sms_receiver_trader(request: Request):
#     """
#     SMS Receiver
#     :param request:
#     :param id:
#     :return:
#     """
#     reqs = await request.body()
#     string = json.loads(reqs.decode("utf-8"))
#     text = string.get('text',0)
#     sender = string.get('smsFrom',0)
#     api_key_from_merchant = request.headers.get('x-api-key')
#     print(api_key_from_merchant)
#     #data_receive = 0
#     print(text)
#     #coalmet
#     user_id = await get_user_from_api_key(api_key_from_merchant)
#     if user_id['data'] > 0:
#         #сбер
#         pattern = r'СБП\s+(\d+)\s*р'
#         #colmet
#         #pattern = r"(\d+\,\d+)\s+(RUB)\s*"
#         #pattern2 = r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})"
#
#         matches = re.search(pattern, text, re.VERBOSE)
#         print(matches)
#         #data = re.search(pattern2, text, re.VERBOSE)
#         if matches:
#             #schet = matches.group(1)
#             suma = matches.group(1).split(" ")
#             print(float(suma[0]))
#
#             valuta = "RUB"
#             # otpravitel = matches.group(4)
#             #datein = data.group(1)
#             #time = data.group(2)
#             # print(f"Счет: {schet}")
#             # print(f"Сумма: {suma} {valuta}")
#             # print(f"Отправитель: {otpravitel}")
#             # print(f"Дата: {datein}")
#             # print(f"Время: {time}")
#             result = {
#                 'user_id': user_id['data'],
#                 'sender': sender,
#                 'sum_fiat': float(suma[0]),
#                 #'datain': datetime.datetime.strptime(datein + " " + time, '%d.%m.%Y %H:%M'),
#                 'datain': datetime.datetime.now(),
#                 'currency': valuta
#             }
#             response = await create_sms_data(result)
#             return response
#
#         else:
#             print("Совпадений не найдено.")
#             return {"Success": False, "data": "Данные не получены"}