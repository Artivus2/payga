from fastapi import APIRouter, HTTPException, Depends, Body
import routers.api_merchant.models as merchant_models
from routers.admin.utils import get_min_amount, send_mail
from routers.api_merchant.controller import (
    get_settings,
    set_settings,
    create_or_update_shop,
    get_shops
)
from routers.mains.controller import get_chart


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


@router.get("/get-settings/{user_id}")
async def get_merchant_settings(user_id: int):
    """
    получить настройки мерчанта
    """
    response = await get_settings(user_id)
    if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
    return response


@router.post("/set-settings")
async def set_merchant_settings(request: merchant_models.Settings):
    """
    установить настройки мерчанта
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await set_settings(payload)
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


@router.get("/get-all-shops/{id}")
async def get_all_shops(id: int):
    """
    вывести магазины
    """
    response = await get_shops(id)
    if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
    return response




