import json

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

from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

#
#
#
#
#
router = APIRouter(prefix='/api/v1/withdrawals', include_in_schema=False, tags=['Вывод средств'])
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


@router.get("/get-wallet-balance")
async def get_admin_balances():
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


#@router.post("/send-to-trx")
def send_transaction():
    full_node = HTTPProvider("https://api.trongrid.io")
    solidity_node = HTTPProvider("https://api.trongrid.io")
    event_server = HTTPProvider("https://api.trongrid.io")
    tron = Tron(provider=full_node)
    private_key = PrivateKey(bytes.fromhex(config.private_key))
    address = private_key.public_key.to_base58check_address()
    token_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT contract address on Tron mainnet
    recipient_address = "TM6hy595DEm9NSzEJ1dLq7ogGeM1Kv4bQA"
    amount = 1  # Amount of USDT to send (in decimal format)
    amount_in_wei = int(amount * 10 ** 6)  # Convert to USDT's decimal precision (6 decimals)

    token_contract = tron.get_contract(token_address)
    transaction = token_contract.functions.transfer(recipient_address, amount_in_wei).build_transaction(
        owner_address=address
    )
    signed_txn = tron.trx.sign(transaction, private_key)
    response = tron.trx.broadcast(signed_txn)
    print(response)

#send_transaction()

#@router.post("/send-to-trx1")
def send_transaction2():
    full_node = HTTPProvider("https://api.trongrid.io")
    client = Tron(provider=full_node)

    with open('abi.json', 'r') as f:  # Замените 'usdt_abi.json' на имя вашего файла
        usdt_abi = json.load(f)
    contract_address = config.USDT_CONTRACT_ADDRESS  # Адрес контракта USDT TRC20
    # #usdt_contract = client.get_contract(usdt_abi, contract_address)
    private_key = PrivateKey.fromhex(config.private_key)
    # from_address = config.admin_wallet
    # sender_address = private_key.public_key.to_base58check_address()
    to_address = 'TM6hy595DEm9NSzEJ1dLq7ogGeM1Kv4bQA'
    #
    # usdt_contract = client.get_contract(config.USDT_CONTRACT_ADDRESS)
    # print(usdt_contract)
    #usdt_contract = client.contract(usdt_abi, contract_address)
    #all_contraat = client.get_contract_info(from_address)
    #print(all_contraat)
    #wallet_balance = get_admin_balance()

    # tx = client.trx.transfer(from_address, to_address, 1).build().sign(private_key)
    # result = tx.broadcast()
    # print(result)
    # print(tx.txid)
    # print(tx.broadcast().wait())
    # tx_hash = client.trx.transfer(to_address, 1, 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',
    #                             fee_limit=10000000)
    # print(tx_hash)
    # try:
    #     tx = (
    #         usdt_contract.functions.transfer(to_address,
    #                                          1 * 10 ** 6)  # умножаем на 10**6, так как USDT TRC20 имеет 6 знаков после запятой
    #         .build()
    #         .sign(private_key)
    #         .broadcast()
    #     )
    #
    #
    #     print(f"Транзакция отправлена: {tx['txid']}")
    # except Exception as e:
    #     print(f"Ошибка при отправке транзакции: {e}")
    # 3 вариант
    contract = client.get_contract(config.USDT_CONTRACT_ADDRESS)
    contract.abi = usdt_abi
    tx = (contract.functions.transfer(to_address, 100000)
          .with_owner(private_key.public_key.to_base58check_address())
          .fee_limit(30000000)
          .build()
          .sign(private_key))
    broadcasted_tx = tx.broadcast().wait()
    try:
        return broadcasted_tx['result'], broadcasted_tx['id']
    except:
        return False, False
    # 4 вариант
    # Amount to transfer
    #amount_to_send = 1 * 10 ** 6  # Amount of USDT to be sent (e.g., 100 USDT)

    # Execute the transfer
    #transaction_hash = transfer_usdt(private_key, to_address, amount_to_send)

#send_transaction2()

def transfer_usdt(private_key, to_address, amount):
    client = Tron()
    # usdt_contract_address = config.USDT_CONTRACT_ADDRESS
    # usdt_contract = client.get_contract(usdt_contract_address)
    # from_address = config.admin_wallet
    # # Build the transaction
    contract = client.get_contract(config.USDT_CONTRACT_ADDRESS)
    tx = (contract.functions.transfer(to_address, 100000)
          .with_owner(private_key.public_key.to_base58check_address())
          .fee_limit(30000000)
          .build()
          .sign(private_key))
    broadcasted_tx = tx.broadcast().wait()
    return broadcasted_tx




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



