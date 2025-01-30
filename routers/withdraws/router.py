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
import time

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


@router.get("/send-to-trx")
def send_transaction():
    # Set up TronGrid provider with the API key directly in the endpoint URL
    api_key = "e4b5469c-1866-4376-8cba-30a15e0218a1"  # Replace with your TronGrid API key
    provider = HTTPProvider(endpoint_uri=f"https://api.trongrid.io?apiKey={api_key}")
    tron = Tron(provider)

    # Set private key and sender's address
    private_key_hex = config.private_key  # Replace with your private key
    private_key = PrivateKey(bytes.fromhex(private_key_hex))
    from_address = private_key.public_key.to_base58check_address()

    usdt_contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    # Get recipient address and amount
    to_address = 'TM6hy595DEm9NSzEJ1dLq7ogGeM1Kv4bQA'
    amount = 0.1

    # Convert the amount to the correct unit (USDT uses 6 decimals)
    amount_in_sun = int(amount * 10 ** 6)

    try:
        # Access the USDT contract
        contract = tron.get_contract(usdt_contract_address)

        # Build and sign the transaction
        txn = (
            contract.functions.transfer(to_address, amount_in_sun)
            .with_owner(from_address)
            .build()
            .sign(private_key)
            .broadcast()

        )

        # Display transaction details
        print("Transaction sent successfully!")
        print("Transaction Hash:", txn["txid"])

        # Wait for confirmation
        print("Waiting for confirmation...")

        # Check if the transaction is confirmed (you can adjust the sleep time or loop for a better polling strategy)
        txn_id = txn["txid"]
        while True:
            txn_info = tron.get_transaction_info(txn_id)
            if txn_info["ret"][0]["contractRet"] == "SUCCESS":
                print("Transaction confirmed!")
                break
            else:
                print("Transaction not yet confirmed. Retrying...")
                time.sleep(10)  # Wait for 10 seconds before checking again

        # Optionally, you can check gas fees here (this part is specific to Tron)
        # Tronscan API can be used to retrieve the transaction details if you need more data about the gas fees
        print(
            "Gas fees and other transaction details can be checked on Tronscan using the txid: https://tronscan.org/#/transaction/" + txn_id)

    except Exception as e:
        print("An error occurred:", e)



