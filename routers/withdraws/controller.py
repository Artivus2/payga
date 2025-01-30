import time

import mysql.connector as cpy
import tronpy
from tronpy.keys import PrivateKey

import config
import telebot
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError


from routers.admin.utils import create_random_key
import telebot
botgreenavipay = telebot.TeleBot(config.telegram_api)
from tronpy.exceptions import AddressNotFound
from tronpy import Tron



async def get_wallet_balance(wallet):
    client = Tron()
    balance = -1
    try:
        token_usdt = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        contract_usdt = client.get_contract(token_usdt)  # usdt
        balance = round(contract_usdt.functions.balanceOf(wallet) / tronpy.TRX, 4)
    except AddressNotFound:
        print("Adress not found..!")

    print(balance)

    return balance

async def get_admin_balance():
    client = Tron()
    wallet_address = config.admin_wallet
    balance = -1
    try:
        token_usdt = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        contract_usdt = client.get_contract(token_usdt)  # usdt
        # search_address = "TWMsYUtqEAPxs7ZXuANkpABqGcixK3XZJD"
        balance = round(contract_usdt.functions.balanceOf(wallet_address) / tronpy.TRX, 4)
    except AddressNotFound:
        print("Adress not found..!")
    print(balance)
    return balance


async def send_transaction_from_admin(payload):
    # private_key = config.private_key
    # from_address = config.admin_wallet
    wallet_balance = await get_admin_balance()
    if wallet_balance > payload.amount:
        # Set up TronGrid provider with the API key directly in the endpoint URL
        tron = Tron()
        # Set private key and sender's address
        private_key_hex = config.private_key  # Replace with your private key
        private_key = PrivateKey(bytes.fromhex(private_key_hex))
        from_address = private_key.public_key.to_base58check_address()

        usdt_contract_address = config.USDT_CONTRACT_ADDRESS

        # Get recipient address and amount
        to_address = payload.to_wallet

        # Convert the amount to the correct unit (USDT uses 6 decimals)
        amount_in_sun = int(payload.amount * 10 ** 6)

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
        return {"Success": True, "data": txn_id}
    else:
        return {"Success": False, "data": "Недостаточно баланса"}


async def send_transaction(payload):

    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            wallet_address = await get_wallet(payload.user_id)
            if wallet_address["Success"]:
                wallet_balance = await get_wallet_balance(wallet_address["data"].get('value'))
                if wallet_balance > payload.amount:
                    # Set up TronGrid provider with the API key directly in the endpoint URL
                    tron = Tron()
                    private_key_hex = wallet_address["data"].get('private_key')
                    private_key = PrivateKey(bytes.fromhex(private_key_hex))
                    from_address = private_key.public_key.to_base58check_address()
                    usdt_contract_address = config.USDT_CONTRACT_ADDRESS
                    amount_in_sun = int(payload.amount * 10 ** 6)
                    try:
                        contract = tron.get_contract(usdt_contract_address)
                        txn = (
                            contract.functions.transfer(payload.to_address, amount_in_sun)
                            .with_owner(from_address)
                            .build()
                            .sign(private_key)
                            .broadcast()
                        )
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

                        print(
                            "Gas fees and other transaction details can be checked on Tronscan using the txid: https://tronscan.org/#/transaction/" + txn_id)

                    except Exception as e:
                        print("An error occurred:", e)

                    return {"Success": True, "data": txn_id}
                else:
                    return {"Success": False, "data": "Недостаточно баланса"}


async def send_to_wallet(order_id, address):
    """
    send USDT from admin wallet from balance to user generated wallet
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_order = "SELECT value FROM pay_orders where id = " + str(order_id)
            cur.execute(string_order)
            order_value = cur.fetchone()[0]
            if order_value:
                result = await send_transaction_from_admin(address, order_value)

                if result:
                    return {"Success": True, "data": result}
                else:
                    return {"Success": False, "data": "Недостаточно баланса"}
            else:
                return {"Success": False, "data": "Ордер не найден"}


async def generate_wallet(payload):

    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if payload.user_id is not None:
                string_check = "SELECT * FROM wallet_address where chain_id = 259 and user_id = " + str(payload.user_id)
                cur.execute(string_check)
                data = cur.fetchone()
                if not data:
                    client = Tron()
                    result = client.generate_address()
                    string = "INSERT into wallet_address (user_id, chain_id, value, private_key, public_key, hex_address)" \
                             " VALUES ('"+str(payload.user_id)+"', 259, '"+str(result['base58check_address'])+"', '" \
                             + str(result['private_key']) + "', '"+str(result['public_key'])+"','" \
                             + str(result['hex_address']) + "')"
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        return {"Success": True, "data": result['base58check_address']}
                    else:
                        return {"Success": False, "data": "Кошелек не сгенерирован"}
                else:
                    return {"Success": False, "data": "на данном аккаунте уже создан кошелек, обратитесь к администратору"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}


async def get_wallet(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_check = "SELECT * FROM wallet_address where user_id = " + str(payload)
            cur.execute(string_check)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Кошелек не найден"}

async def get_admin_wallet_address():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_check = "SELECT user.id, user.login, wallet_address.value FROM user " \
                           "LEFT JOIN wallet_address ON user.id = wallet_address.user_id where role_id = 1 "
            cur.execute(string_check)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Кошелек не найден"}
