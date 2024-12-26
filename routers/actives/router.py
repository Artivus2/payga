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
    get_pay_type_by_id,
    crud_transfer,
    get_balance_history_statuses,
    get_balance_history_historyes,
    dep_withdrawal_check,
    bal_withdrawal_check,
    get_deposit_history_statuses,
    bal_refunds_check

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

    }
    """
    print(request)
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
    user_id: int
    }
    """

    response = await crud_balance('create', request)
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
    frozen: float
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
    baldep_status_id: int
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


@router.post("/change-balance-frozen")
async def change_balance_frozen(request: actives_models.Balance):
    """
    :param request:
    :return:
    {
    user_id: int
    value: float
    }
    """
    response = await crud_balance('frozen', request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/change-balance-unfrozen")
async def change_balance_unfrozen(request: actives_models.Balance):
    """
    :param request:
    :return:
    {
    user_id: int
    value: float
    }
    """
    response = await crud_balance('unfrozen', request)
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
    :param request: only for admin
    :return:
    {
    user_id: int
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
    :param request: only for admin
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


@router.post("/set-min-deposit")
async def set_deposit(request: actives_models.Deposit):
    """
    :param request: only for admin
    :return:
    {
    user_id: int
    value: float
    }
    """
    response = await crud_deposit('set-min', request)
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



@router.post("/refunds-balance")
async def balance_in(request: actives_models.Balance):
    """
    запрос вывода с баланса в сеть
    :param request:
    :return:
    """
    response = await bal_refunds_check(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.post("/withdrawals-from-balance")
async def from_balance(request: actives_models.Balance):
    """
    запрос вывода с баланса в сеть
    :param request:
    :return:
    """
    response = await bal_withdrawal_check(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.post("/withdrawals-from-deposit")
async def from_deposit(request: actives_models.Deposit):
    """
    вывод с депозита после не менее 1 месяца после 1 пополнения баланса (из истории)
    """
    response = await dep_withdrawal_check(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-deposit-statuses")
async def get_deposit_history_status(request: actives_models.DepositHistoryStatus):
    """
    :param request:
    :return:
    """
    response = await get_deposit_history_statuses()
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


@router.post("/change-deposit-frozen")
async def change_deposit_frozen(request: actives_models.Deposit):
    """
    :param request:
    :return:
    {
    user_id: int
    frozen: float
    }
    """
    response = await crud_deposit('frozen', request)
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
@router.get("/get-balance-history/{user_id}")
async def get_balance_history(user_id: int | None):
    """
    :param user_id: 0 - для админа по всем история
    :param request:
    :return:
    {
    id: int
    user_id: int
    balance_id: int
    chart: str
    date: int
    value: float
    frozen: float
    balance_history_status_id: int
    description: str
    }
    """
    response = await get_balance_history_historyes(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-balance-history-statuses")
async def get_balance_history_status():
    """
    :param request:
    :return:
    {
    id: int
    title: str
    }
    """
    response = await get_balance_history_statuses()
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


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
    frozen: float
    balance_history_status_id: int
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
    }
    """
    pass


@router.post("/create-transfer")
async def create_transfer(request: actives_models.TransferHistory):
    """
    :param request:
    :return:
    {
    user_id_in_email_or_login: str (кому переводим)
    user_id_out_email_or_login: str (от кого переводим)
    value: float
    }
    """
    response = await crud_transfer("create", request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-transfers/{user_id}")
async def get_transfer(user_id: int):
    """
    :param user_id:
    :param request:
    :return:
    {
    user_id: 0 - все
    }
    """
    response = await crud_transfer("get", user_id)
    print(response)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



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
async def get_baldeps_status(id: int):
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
async def get_baldeps_types(id: int):
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



