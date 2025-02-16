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

from routers.actives.controller import crud_balance
from routers.admin.controller import (
    get_user_from_api_key,
    create_sms_data,
    get_info_for_invoice,
    get_pattern,
    get_trader_user_id,
    get_payment_status,
    get_payout_status,
    get_data_sms

)
from routers.admin.utils import create_access_token, get_min_amount
from routers.api_merchant.controller import save_history_payment, save_history_payout
from routers.mains.controller import get_chart
from routers.nowpayments.controller import get_jwt_token
from routers.orders.controller import (
    create_order_for_user_payin,
    insert_docs,
    create_order_for_user_payout)
from routers.orders.utils import generate_uuid

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



@router.get("/get-payment-status/{uuids}")
async def get_payment(uuids: str):
    """
    uuid
    """
    response = await get_payment_status(uuids)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.get("/get-payout-status/{order_id}")
async def get_payout(order_id: str):
    """
    o_id
    """
    response = await get_payout_status(order_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
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



@router.post("/create-payment")
async def create_payin_order_for_trader(request: Request):
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
    req_id = string.get('req_id')
    get_trader_by_chosen_req = await get_trader_user_id(req_id)
    result_from_payment = {
        "req_id": req_id, #user_id_trader из reqs
        "sum_fiat": string.get('sum_fiat'),
        "o_id": string.get('o_id'),
        'user_id_trader': get_trader_by_chosen_req, #user_trader
        'user_id_merchant': user_id['data'],  # user_trader
        'pay_id': 1, # payin,
        'docs_id': string.get('docs_id', 0)
    }

    response = await create_order_for_user_payin(result_from_payment)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/create-payout")
async def create_payout_order_for_trader(request: Request):
    """
    Creates a payout for trader. With this method,
    the customer is required to withdrawals funds.

    :return:
    """
    api_key_from_merchant = request.headers.get('x-api-key')
    reqs = await request.body()
    print(reqs)
    string = json.loads(reqs.decode("utf-8"))
    user_id = await get_user_from_api_key(api_key_from_merchant)
    result_from_payout = {
        "sum_fiat": string.get('sum_fiat'),
        'receiver': string.get('receiver'),
        'o_id': string.get('o_id'),
        'user_id_merchant': user_id['data'],
        'docs_id': string.get('docs_id', 0)
    }
    response = await create_order_for_user_payout(result_from_payout)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-sms-data/{user_id}")
async def sms_receiver_from_db(user_id: int):
    """
    получить данные
    """
    response = await get_data_sms(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
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
    print(string, request.headers.get('x-api-key'))
    text = string.get('body')
    sender = string.get('address')
    api_key_from_trader = request.headers.get('x-api-key')
    user_id = await get_user_from_api_key(api_key_from_trader)
    if user_id['Success']:
        result = await get_pattern(sender, text)

        if result['Success']:
            result["user_id_trader"] = user_id['data']

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


@router.post("/refunds")
async def refunds_trader_into_balance(request: trader_models.CreatePaymentRequest):
    """
    пополнение баланса трейдера (в usdt)
    """
    url = f"{config.base_url_np}payment"
    headers = {
        "x-api-key": config.api_key_np,
        "Content-Type": "application/json"
    }
    order_uuid = await generate_uuid()
    payload = {
        "price_amount": request.amount,
        "price_currency": 'usd',
        "order_id": order_uuid,
        "pay_currency": 'usdttrc20'
    }
    print(payload)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())

    payload2 = {
        "user_id": request.user_id,
        "price_amount": request.amount,
        "order_uuid": order_uuid,
        "payment_id": response.json()["payment_id"],
        "payment_status": response.json()["payment_status"],
        "type": 1
    }

    if request.amount >= 10:
        result = await save_history_payment(payload2)
        if result["Success"]:
            return {"data": result["data"]}
        else:
            raise HTTPException(status_code=response.status_code, detail="Не удалось получить данные")
    else:
        raise HTTPException(status_code=400, detail="Минимальная сумма 10 usdt")


@router.post("/withdrawals")
async def create_withdrawals_trader_from_balance(request: trader_models.CreatePayoutRequest):
    """
    вывод баланса трейдера в (usdt)
    """

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
                'currency': 'usdttrc20'
                #'ipn_callback_url': 'https://greenavi.com/api/payment/notice-ipn'  # Your IPN callback URL
            }
        ]
    }
    order_uuid = await generate_uuid()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    try:
        id = response.json()['batch_withdrawal_id']
    except:
        id = 0
    if id == 0:
        raise HTTPException(status_code=response.status_code, detail="Не удалось создать заявку на вывод")
    print(response.json())
    payload2 = {
        "user_id": request.user_id,
        "price_amount": request.amount,
        "order_uuid": order_uuid,
        "payout_id": response.json()["withdrawals"][0]["id"],
        "payout_status": response.json()["withdrawals"][0]["status"],
        "type_id": 2
    }
    print(payload2)
    result  = await save_history_payout(payload2)
    if result["Success"]:
        return {"data": result["data"]}
    else:
        raise HTTPException(status_code=response.status_code, detail="Не удалось получить данные")


