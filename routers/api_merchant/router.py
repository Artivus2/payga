import json
from fastapi import APIRouter, HTTPException, Depends, Body
import config
import routers.api_merchant.models as merchant_models
import requests

from routers.actives.controller import crud_balance
from routers.admin.utils import get_min_amount, send_mail
from routers.api_merchant.controller import (
    getfavtypes,
    setfavtypes,
    create_or_update_shop,
    get_shops,
    save_history_payment,
    save_history_payout,
    #get_payment_status_by_uuid
)
from routers.mains.controller import get_chart
from routers.nowpayments.controller import get_jwt_token
from routers.orders.utils import generate_uuid

router = APIRouter(prefix='/api/v1/merchant',
                   tags=['Мерчант'],
                   #dependencies=[Depends(merchant_models.GetApiKey())]
                   )

@router.get("/get-api-status")
async def get_api_status():
    """
    https://pay.greenavi.com/api/v1/merchant/get-api-status
    Проверка статуса API
    :param request:
    :return:
    """
    #await send_mail('тестовое сообщение', 'тестовая тема', 'artivus@gmail.com')

    return {"Success": True, "data": "API доступна"}


# @router.post("/authentication")
# async def authentication_by_api_key(request: user_models.User):
#     """
#     Доступ к системе по API_KEY
#     This set of methods allows you to check API availability and get a JWT token which is
#     requires as a header for some other methods
#     :param api_key:
#     :return:
#     """
#     print(request)
#     access_token = create_access_token(user_id=request.email,
#                                        role=request['data']['role_id'],
#                                        expires_delta=config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     return {"Succees": True, "data": access_token}


@router.get("/get-available-currencies")
async def get_charts():
    """
    https://pay.greenavi.com/api/v1/merchant/get-available-currencies
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
    https://pay.greenavi.com/api/v1/merchant/min-amount
    Get the minimum payment amount
    HEADERS
    x-api-key: {{api-key}}

    (Required) Your PayGreenavi API key
    :return:
    """
    response = await get_min_amount()
    return response


@router.get("/get-fav-reqs-types/{shop_id}")
async def get_merchant_settings(shop_id: int):
    """
    получить настройки мерчанта
    """
    response = await getfavtypes(shop_id)
    if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
    return response


@router.post("/set-fav-reqs-types")
async def set_merchant_settings(request: merchant_models.FavReqsTypes):
    """
    установить настройки мерчанта
    """
    response = await setfavtypes(request)
    if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
    return response


@router.post("/create-shops")
async def create_shops(request: merchant_models.Shops):
    """
    Создать магазин
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    if request.id is None:
        payload['id'] = 0
    print(payload)
    response = await create_or_update_shop(payload)
    if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
    return response


@router.get("/get-all-shops/{user_id}/{id}")
async def get_all_shops(id: int | None, user_id: int):
    """
    вывести магазины
    """
    response = await get_shops(id, user_id)
    if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
    return response

@router.post("/create-payment")
async def create_payment(request: merchant_models.CreatePaymentRequest):
    """
    пополнение баланса мерчанта в (usdt)
    """
    url = f"{config.base_url_np}payment"
    headers = {
        "x-api-key": config.api_key_np,
        "Content-Type": "application/json"
    }
    order_uuid =  await generate_uuid()
    payload = {
        "price_amount": request.amount,
        "price_currency": 'usd',
        "order_id":order_uuid,
        "pay_currency": 'usdttrc20'
    }
    if request.amount >= 10:
        print(payload)
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response.json())

        payload2 = {
            "user_id": request.user_id,
            "price_amount": request.amount,
            "order_uuid": order_uuid,
            "payment_id": response.json()["payment_id"],
            "payment_status": response.json()["payment_status"],
            "type_id": 1
        }
        print(payload2)
        result  = await save_history_payment(payload2)
        if result["Success"]:
            return {"data": result["data"]}
        else:
            raise HTTPException(status_code=response.status_code, detail="Не удалось получить данные")
    else:
        raise HTTPException(status_code=400, detail="Минимальная сумма 10 usdt")



@router.post("/create-payout")
async def create_payout_merchant(request: merchant_models.CreatePayoutRequest):
    """
    вывод баланса мерчанта в (usdt)
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
    print(response.json())
    try:
        id = response.json()['id']
    except:
        id = 0
    if id == 0:
        raise HTTPException(status_code=response.status_code, detail="Не удалось создать заявку на вывод")
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



