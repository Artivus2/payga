import json
from typing import Optional

import routers.actives.models as actives_models
import requests
from fastapi import APIRouter, HTTPException
import config
from routers.actives.controller import (
    crud_balance_percent,
    crud_balance,
    crud_deposit,
    get_transfer_status_by_id,
    get_wallet_status_by_id,
    get_baldep_types_by_id,
    get_baldep_status_by_id,
    get_pay_status_by_id,
    get_pay_type_by_id
)

router = APIRouter(prefix='/api/v1/actives', tags=['Активы'])


### percent ###
@router.post("/create-balance-percent")
async def create_balance_percent(request: dict):
    """
    Создать процент payin или payout
    :param request:
    :return:
    {
    user_id: int
    pay_id: int
    value: float
    date: int
    pay_status_id: int
    }
    """
    response = await crud_balance_percent('create', request)
    print(response)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-balance-percent/{user_id}")
async def get_balance_percent(user_id: int):
    """
    Получить баланс
    :param user_id:
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance_percent('get', user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.put("/set-balance-percent")
async def set_balance_percent(request: actives_models.PayPercent):
    """
    установить процент payin или payout
    :param request:
    :return:
    {
    id: int
    user_id: int
    pay_id: int
    percent: float
    date: int
    pay_status_id: int
    }
    """
    response = await crud_balance_percent('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.delete("/remove-balance-percent")
async def remove_balance_percent(request: actives_models.PayPercent):
    """
    Удалить процент payin или payout
    :param request:
    :return:
    {
    id: int
    user_id: int
    pay_id: int
    percent: float
    date: int
    pay_status_id: int
    }
    """
    response = await crud_balance_percent('remove', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


### balance ###
@router.post("/create-balance")
async def create_balance(request: actives_models.Balance):
    """
    Создать баланс
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    print(request)
    response = await crud_balance('create', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


@router.get("/get-balance/{user_id}")
async def get_balance(user_id: int):
    """
    Получить баланс
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('get', user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.put("/set-balance")
async def set_balance(request: actives_models.Balance):
    """
    Update баланс
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


@router.delete("/remove-balance")
async def remove_balance(request: actives_models.Balance):
    """
    удалить баланс
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('remove', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()

#deposit
@router.post("/create-deposit")
async def create_deposit(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    id: int
    value: float
    user_id: int
    status: int
    types: int
    }
    """
    response = await crud_deposit('create', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


@router.get("/get-deposit/{user_id}")
async def get_deposit(user_id: int):
    """
    Получить баланс
    :param user_id:
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_deposit('get', user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.put("/set-deposit")
async def set_deposit(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    id: int
    value: float
    user_id: int
    status: int
    types: int
    }
    """
    response = await crud_deposit('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


@router.delete("/remove-deposit")
async def remove_deposit(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    id: int
    value: float
    user_id: int
    status: int
    types: int
    }
    """
    response = await crud_deposit('remove', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()

# wallet
@router.post("/create-wallet")
async def create_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {id: int
    user_id: int
    network: str
    address: str
    wallet_status: int
    date: int}
    """
    pass


@router.get("/get-wallet")
async def get_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {id: int
    user_id: int
    network: str
    address: str
    wallet_status: int
    date: int}
    """
    pass


@router.put("/set-wallet")
async def set_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {id: int
    user_id: int
    network: str
    address: str
    wallet_status: int
    date: int}
    """
    pass


@router.delete("/remove-wallet")
async def remove_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {id: int
    user_id: int
    network: str
    address: str
    wallet_status: int
    date: int}
    """
    pass


# balance history
@router.get("/get-balance-history")
async def get_balance_history(request: actives_models.BalanceHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id: int
    balance_id: int
    chart: str
    date: int
    value: float
    balance_status_id: int
    balance_types_id: int
    description: str
    }
    """
    pass


@router.put("/set-balance-history")
async def set_balance_history(request: actives_models.BalanceHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id: int
    balance_id: int
    chart: str
    date: int
    value: float
    balance_status_id: int
    balance_types_id: int
    description: str
    }
    """
    pass


@router.delete("/remove-balance-history")
async def remove_balance_history(request: actives_models.BalanceHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id: int
    balance_id: int
    chart: str
    date: int
    value: float
    balance_status_id: int
    balance_types_id: int
    description: str
    }
    """
    pass


@router.post("/create-transfer")
async def create_transfer(request: actives_models.TransferHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id_in: int
    user_id_out: int
    value: float
    status: int
    }
    """
    pass


@router.get("/get-transfer")
async def get_transfer(request: actives_models.TransferHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id_in: int
    user_id_out: int
    value: float
    status: int
    }
    """
    pass


@router.put("/set-transfer")
async def set_transfer(request: actives_models.TransferHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id_in: int
    user_id_out: int
    value: float
    status: int
    }
    """
    pass


@router.delete("/remove-transfer")
async def remove_transfer(request: actives_models.TransferHistory):
    """
    :param request:
    :return:
    {
    id: int
    user_id_in: int
    user_id_out: int
    value: float
    status: int
    }
    """
    pass


@router.post("/create-exchange")
async def create_exchange(request: actives_models.ExchangeHistory):
    """
    :param request:
    :return:
    {
    id: int
    chart_in_id: int
    chart_out_id: int
    date: int
    value: float
    course: float
    }
    """
    pass


@router.get("/get-exchange")
async def get_exchange(request: actives_models.ExchangeHistory):
    """
    :param request:
    :return:
    {
    id: int
    chart_in_id: int
    chart_out_id: int
    date: int
    value: float
    course: float
    }
    """
    pass


@router.put("/set-exchange")
async def set_exchange(request: actives_models.ExchangeHistory):
    """
    :param request:
    :return:
    {
    id: int
    chart_in_id: int
    chart_out_id: int
    date: int
    value: float
    course: float
    }
    """
    pass


@router.delete("/remove-exchange")
async def remove_exchange(request: actives_models.ExchangeHistory):
    """
    :param request:
    :return:
    {
    id: int
    chart_in_id: int
    chart_out_id: int
    date: int
    value: float
    course: float
    }
    """
    pass


@router.get("/get-pay-type/{id}")
async def get_pay_type(id: int):
    """
    payin, payout
    :param id:
    :return:
    """
    response = await get_pay_type_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/get-pay-status/{id}")
async def get_pay_status(id: int):
    """
    Действующий (1), не действующий (2), 0 - все
    :param id:
    :return:
    """
    response = await get_pay_status_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/get-baldep-status/{id}")
async def get_balance_status(id: int):
    """
    title: 1 - доступно, 2 - замороженоm 0 - все
    :param id:
    :return:
    """
    response = await get_baldep_status_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-baldep-types/{id}")
async def get_balance_types(id: int):
    """
    title: 1 - активные, 2 - архивные, 0 - все
    :param id:
    :return:
    """
    response = await get_baldep_types_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/get-wallet-status/{id}")
async def get_wallet_status(id: int):
    """
    Активный (1) / не активный (2), 0 - все
    :param id:
    :return:
    """
    response = await get_wallet_status_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/get-transfer-status/{status_id}")
async def get_transfer_status(status_id: int):
    """
    status: исполнен (1), отменен (2), в ожидании (3), 0 - все
    :param skip:
    :param status_id:
    :return:
    """
    response = await get_transfer_status_by_id(status_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response

