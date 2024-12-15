import mysql.connector as cpy
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

async def get_admin_balance():
    client = Tron()
    wallet_admin = config.admin_wallet
    balance = -1
    try:
        balance = client.get_account_balance(wallet_admin)
    except AddressNotFound:
            print( "Adress not found..!")
    print(balance)
    return balance




async def send_transaction(to_address, amount):
    #учетные данные из config админа адрес
    private_key = config.private_key
    from_address = config.admin_wallet
    wallet_balance = get_admin_balance()
    if wallet_balance > amount:
        #Отправка USDT
        client = Tron()

        tx = client.trx.transfer(from_address, to_address, amount).build().sign(private_key)
        result = tx.broadcast()
        print(result)
        print(tx.txid)
        print(tx.broadcast().wait())
        #save transaction to db

        return True
    else:
        return False

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
                result = send_transaction(address, order_value)

                if result:
                    return True
                else:
                    return False

async def generate_wallet(payload):
    client = Tron()
    result = client.generate_address()
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if payload.user_id is not None:
                string_check = "SELECT * FROM wallet_address where user_id = " + str(payload.user_id)
                cur.execute(string_check)
                data = cur.fetchone()
                if not data:
                    string = "INSERT into wallet_address (user_id, chain_id, value, private_key, public_key, hex_address)" \
                             " VALUES ('"+str(payload.user_id)+"', 259, '"+str(result['base58check_address'])+"', '" \
                             + str(result['private_key']) + "', '"+str(result['public_key'])+"','" \
                             + str(result['hex_address']) + "')"
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        return {"Success": True, "data": "Кошелек сгенерирован"}
                    else:
                        return {"Success": False, "data": "Кошелек не сгенерирован"}
                else:
                    return {"Success": False, "data": "на данном аккаунте уже создан кошелек, обратитесь к администратору"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}

async def get_wallet(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_check = "SELECT value FROM wallet_address where user_id = " + str(payload)
            cur.execute(string_check)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data.get('value')}
            else:
                return {"Success": False, "data": "Кошелек не найден"}





