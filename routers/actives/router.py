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
    crud_wallet,
    get_transfer_status_by_id,
    get_baldep_types_by_id,
    get_baldep_status_by_id,
    get_pay_status_by_id,
    get_pay_type_by_id

)

router = APIRouter(prefix='/api/v1/actives', tags=['Активы'])


### percent ###
@router.post("/create-balance-percent")
async def create_balance_percent(request: actives_models.PayPercent):
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


@router.post("/get-balance-percent")
async def get_balance_percent(request: actives_models.PayPercent):
    """
    Получить % баланс
    :param user_id:
    :param request:
    :return:
    {
    user_id: int
    pay_id: int
    value: float
    date: str
    pay_status_id: int
    }
    """
    response = await crud_balance_percent('get', request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-balance-percent")
async def set_balance_percent(request: actives_models.PayPercent):
    """
    установить процент payin или payout
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
    response = await crud_balance_percent('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-balance-percent")
async def remove_balance_percent(request: actives_models.PayPercent):
    """
    Удалить процент payin или payout
    :param request:
    :return:
    {
    pay_status_id: int
    }
    """
    response = await crud_balance_percent('remove', request.pay_status_id)
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
    chart_id: int
    baldep_status_id: int
    baldep_types_id: int
    }
    """

    payload = {
        'id': request.id,
        'user_id': request.user_id,
        'chart_id': request.chart_id,
        'value': request.value,
        'baldep_status_id': request.baldep_status_id,
        'baldep_types_id': request.baldep_types_id
    }
    response = await crud_balance('create', payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/get-balance")
async def get_balance(request: actives_models.Balance):
    """
    Получить баланс по user_id
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('get', request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-balance")
async def set_balance(request: actives_models.Balance):
    """
    Update баланс
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-balance")
async def remove_balance(request: actives_models.Balance):
    """
    удалить баланс
    :param request:
    :return:
    {
    id: int
    user_id: int
    value: float
    chart_id: int
    balance_status_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('remove', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.post("/change-balance-status")
async def change_balance_status(request: actives_models.Balance):
    """
    :param request:
    :return:
    {
    user_id: int
    balance_status_id: int
    }
    """
    response = await crud_balance('status', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/change-balance-type")
async def change_balance_type(request: actives_models.Balance):
    """
    :param request:
    :return:
    {
    user_id: int
    balance_types_id: int
    }
    """
    response = await crud_balance('type', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


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
    balance_status_id: int
    balance_types_id: int
    description: str
    }
    """
    response = await crud_deposit('create', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/get-deposit")
async def get_deposit(request: actives_models.Deposit):
    """
    Получить баланс
    :param user_id:
    :param request:
    :return:
    {
    user_id: int
    }
    """
    response = await crud_deposit('get', request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-deposit")
async def set_deposit(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    user_id: int
    value: float
    }
    """
    response = await crud_deposit('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-deposit")
async def remove_deposit(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    user_id: int
    }
    """
    response = await crud_deposit('remove', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/change-deposit-status")
async def change_deposit_status(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    user_id: int
    balance_status_id: int
    }
    """
    response = await crud_deposit('status', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/change-deposit-type")
async def change_deposit_type(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    user_id: int
    balance_types_id: int
    }
    """
    response = await crud_deposit('type', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


# wallet
@router.post("/create-wallet")
async def create_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {
    user_id: int
    network: str
    address: str
    }
    """
    response = await crud_wallet('create', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/get-wallet")
async def get_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {
    user_id: int (0 - все, только для админ?)
    }
    """
    response = await crud_wallet('get', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/get-wallet-statuses")
async def get_wallet(request: actives_models.WalletStatus):
    """
    :param request:
    :return:
    {
    id: int (0)
    }
    """
    response = await crud_wallet('status', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-wallet-status")
async def set_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {
    user_id: int
    wallet_status: int
    }
    """
    response = await crud_wallet('set', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-wallet")
async def remove_wallet(request: actives_models.Wallet):
    """
    :param request:
    :return:
    {
    user_id: int

    }
    """
    response = await crud_wallet('remove', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


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


@router.get("/get-balance-history-statuses")
async def get_balance_history_statuses(request: actives_models.BalanceHistoryStatus):
    """
    :param request:
    :return:
    {
    id: int
    title: str
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

