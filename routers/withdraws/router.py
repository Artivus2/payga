import json

from fastapi import APIRouter, HTTPException
import requests

#
import config
import routers.withdraws.models as withdraws_models
from routers.withdraws.controller import (
    generate_wallet,
    get_wallet_balance,
    send_transaction,
    send_transaction_from_admin,
    get_wallet,
    get_admin_wallet_address

)


router = APIRouter(prefix='/api/v1/withdrawals', include_in_schema=False, tags=['Крипто операции'])

@router.get("/get_admin_address")
async def get_admins_wallets():
    """
    Получить адреса USDT trc20 админов для пополнения средств
    :param request:
    :return:
    """

    response = await get_admin_wallet_address()
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/check-wallet-balance/{wallet}")
async def get_wallet_balances(wallet: str):
    """
    check usdt tron wallet balance
    :param request:
    :return:
    """

    response = await get_wallet_balance(wallet)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.post("/generate-wallet-tron")
async def gen_wallet_tron(request: withdraws_models.WalletAddress):
    """
    generate usdt tron wallet
    :param request:
    :return:
    """

    response = await generate_wallet(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-wallet-address/{user_id}")
async def get_wallet_users(user_id: int):
    response = await get_wallet(user_id)
    return response


@router.get("/validate_address/{address}")
async def validate_address(address: str):
    url = "https://api.shasta.trongrid.io/wallet/validateaddress"

    payload = {
        "address": address,
        "visible": True
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    return response.json()
#


@router.post("/send-to-user-wallet")
async def send_transacs(request: withdraws_models.SendTransactions):

    response = await send_transaction(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/send-transaction-from-admin")
async def send_transaction_admin(request: withdraws_models.SendTransactions):
    response = await send_transaction_from_admin(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response




