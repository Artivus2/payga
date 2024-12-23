import json

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import RedirectResponse
from typing import Any

from starlette.responses import HTMLResponse

import routers.api_merchant.models as merchant_models
from routers.admin.controller import get_user_from_api_key
from routers.admin.utils import get_min_amount
from routers.mains.controller import get_chart
from starlette.requests import Request

from routers.orders.controller import create_order_for_user

router = APIRouter(prefix='/api/v1/merchant',
                   tags=['Мерчант'],
                   dependencies=[Depends(merchant_models.GetApiKey())]
                   )

@router.get("/get-api-status")
async def get_api_status():
    """
    https://pay.greenavi.com/api/v1/merchant/get-api-status
    Проверка статуса API
    :param request:
    :return:
    """
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


@router.get("/get-payment-status/{payment_id}")
async def get_payment_status(payment_id: int):
    """
    waiting - waiting for the customer to send the payment. The initial status of each payment;
    confirming - the transaction is being processed on the blockchain. Appears when pay.greenavi.com
                detect the funds from the user on the blockchain;
    confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations;
    sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you;
    finished - the funds have reached your personal address and the payment is finished;
    failed - the payment wasn't completed due to the error of some kind;
    refunded - the funds were refunded back to the user;
    expired - the user didn't send the funds to the specified address in the 7 days time window;
    :return:
    """
    pass


@router.get("/get-payment-list")
async def get_payment_list():
    """
    List of orders
    :return:
    """


