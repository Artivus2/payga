from fastapi import APIRouter, HTTPException
import requests

#
import config
import routers.withdraws.models as withdraws_models
from routers.withdraws.controller import (
    get_admin_balance,
    generate_wallet,
    get_wallet

)

from tronpy.exceptions import AddressNotFound
from tronpy import Tron
from tronpy.keys import PrivateKey
#
#
#
#
#
router = APIRouter(prefix='/api/v1/withdrawals', tags=['Вывод средств'])
#
#
# @router.post("/check-balance")
# async def get_stats(request: withdraws_models.Withdraws):
#     pass
#
#
# @router.post("/balance-out")
# async def get_stats(request: withdraws_models.Withdraws):
#     pass
#
@router.post("/generate-wallet-tron")
async def get_wallet_tron(request: withdraws_models.WalletAddress):
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


@router.get("/get-wallet-balance/{address}")
async def get_admin_balances(address: str):
    response = await get_admin_balance()
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
#
@router.post("/send-to-trx")
async def send_transaction(request: withdraws_models.Withdraws):
    client = Tron()
    private_key = PrivateKey.fromhex(config.private_key)
    from_address = config.admin_wallet
    sender_address = private_key.public_key.to_base58check_address()

    usdt_contract = client.get_contract(config.USDT_CONTRACT_ADDRESS)
    #all_contraat = client.get_contract_info(from_address)
    #print(all_contraat)
    #wallet_balance = get_admin_balance()
    to_address = 'TM6hy595DEm9NSzEJ1dLq7ogGeM1Kv4bQA'
    # tx = client.trx.transfer(from_address, to_address, 1).build().sign(private_key)
    # result = tx.broadcast()
    # print(result)
    # print(tx.txid)
    # print(tx.broadcast().wait())
    try:
        tx = (
            usdt_contract.functions.transfer(to_address,
                                             1 * 10 ** 6)  # умножаем на 10**6, так как USDT TRC20 имеет 6 знаков после запятой
            .build()
            .sign(private_key)
            .broadcast()
        )


        print(f"Транзакция отправлена: {tx['txid']}")
    except Exception as e:
        print(f"Ошибка при отправке транзакции: {e}")


#
#
# @router.post(("/get-transaction-history"))
# async def get_transactions_by_wallet(request: withdraws_models.Withdraws):
#     """
#     USDT TRC20
#     :param request:
#     :return:
#     """
#     pass


