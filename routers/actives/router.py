import json
import routers.actives.models as actives_models
import requests
from fastapi import APIRouter, HTTPException
import config
from routers.actives.controller import (
    crud_balance_percent,
    crud_balance,
    crud_deposit
)

router = APIRouter(prefix='/api/v1/actives', tags=['Actives'])


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


@router.get("/get-balance-percent")
async def get_balance_percent(request: actives_models.PayPercent):
    """
    Получить процент payin или payout
    :param user_id:
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
    print(request)

    response = await crud_balance_percent('get', request)
    print(response)
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
    response = await crud_balance('create', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


@router.post("/get-balance")
async def get_balance(request: actives_models.Balance):
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
    response = await crud_balance('get', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


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


@router.post("/get-deposit")
async def get_deposit(request: actives_models.Deposit):
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
    response = await crud_deposit('get', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    return response.json()


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
