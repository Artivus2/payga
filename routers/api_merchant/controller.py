import mysql.connector as cpy
import config
import requests
from routers.admin.utils import create_random_key
from routers.orders.utils import generate_uuid
from fastapi import APIRouter, HTTPException, Depends, Body


async def getfavtypes(shop_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:

            check_settings = "SELECT * FROM pay_fav_merchant_reqs_types " \
                              "LEFT JOIN pay_reqs_types ON pay_reqs_types.id = pay_fav_merchant_reqs_types.pay_reqs_types_id" \
                              " where shop_id = " + str(shop_id)
            cur.execute(check_settings)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось найти параметры"}


async def setfavtypes(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT * from pay_fav_merchant_reqs_types where " \
                           "shop_id = " + str(payload.shop_id) + " and pay_reqs_types_id = " + str(payload.pay_reqs_types_id)
            cur.execute(check_string)
            fav_reqs = cur.fetchall()
            if fav_reqs:
                update_string = "UPDATE pay_fav_merchant_reqs_types set " \
                                "active = '" + str(payload.active) + "' where shop_id = " + str(payload.shop_id) \
                                + " and pay_reqs_types_id = " + str(payload.pay_reqs_types_id)
                cur.execute(update_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Статус активности изменен"}
                else:
                    return {"Success": False, "data": "Платежный метод не изменен"}
            else:
                insert_string = "INSERT INTO pay_fav_merchant_reqs_types (shop_id, pay_reqs_types_id, active) " \
                                "VALUES (" + str(payload.shop_id) + \
                                ",'" + str(payload.pay_reqs_types_id) + "', 1)"
                cur.execute(insert_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно добавлен в группу избранных платежных методов"}
                else:
                    return {"Success": False, "data": "платежный метод не добавлен не добавлен"}


async def remove_fav_reqs(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            delete_string = "DELETE FROM pay_fav_merchant_reqs_types where " \
                            "id = '"+str(payload.id) + "'"
            cur.execute(delete_string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно удален из группы избранных платежных методов"}
            else:
                cnx.close()
                return {"Success": False, "data": "платежный метод не найден"}



async def create_or_update_shop(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if payload.get('id') != 0:
                id = 0
                data_update = "UPDATE pay_shops SET "
                for k, v in dict(payload).items():
                    if k != 'id':
                        data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where id = " + str(payload.get('id'))
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно обновлены данные"}
                else:
                    return {"Success": False, "data": "Данные не обновлены"}
            else:
                uuids = await generate_uuid()
                secret_word = await create_random_key(20)
                data_insert = "INSERT into pay_shops (uuid, user_id, title, balance, date, site_url, success_url, fail_url, secret_word " \
                              ") VALUES ('" \
                              + str(uuids) + "', '" + str(payload.get('user_id')) + "', '" + str(
                                payload.get('title')) + "', 0, UTC_TIMESTAMP(), '"+str(payload.get('site_url')) \
                                + "', '" + str(payload.get('success_url')) \
                                + "', '" + str(payload.get('fail_url')) + "', '" + str(secret_word) + "')"
                cur.execute(data_insert)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно обновлен магазин"}
                else:
                    return {"Success": False, "data": "магазин не обновлен"}



async def get_shops(id, user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_settings = "SELECT * FROM pay_shops"
            dop1 = ""
            if id != 0:
                dop1 = " where id = " + str(id)
            else:
                dop1 = " where id > 0"

            if user_id != 0:
                dop1 += " and user_id = " + str(user_id)
            else:
                dop1 = " and user_id > 0"


            check_settings += dop1
            cur.execute(check_settings)


            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось найти магазин"}



async def save_history_payment(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            status =payload.get('payment_status')
            print(status)
            string = "SELECT * FROM user where id = " + str(payload.get('user_id'))
            cur.execute(string)
            data0 = cur.fetchone()
            if data0:
                history = "INSERT into pay_history (user_id, np_order_uuid, value, date, status, payment_id, type) " \
                "VALUES ('" + str(payload.get('user_id')) + "','" + str(payload.get('order_uuid')) + \
                "','" + str(payload.get('price_amount')) + "',UTC_TIMESTAMP(), '"+str(status)+ \
                          "', '" + str(payload.get('payment_id')) + "', 1)"
                cur.execute(history)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": payload.get('payment_id')}
                else:
                    return {"Success": False, "data": "Данных нет"}
            else:
                return {"Success": False, "data": "Заявка не найдена"}



async def save_history_payout(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            status =payload.get('payout_status')
            print(status)
            string = "SELECT * FROM user where id = " + str(payload.get('user_id'))
            cur.execute(string)
            data0 = cur.fetchone()
            if data0.get('twofa_status') == 1:
                if data0:
                    history = "INSERT into pay_history (user_id, np_order_uuid, value, date, status, payment_id, type) " \
                    "VALUES ('" + str(payload.get('user_id')) + "','" + str(payload.get('order_uuid')) + \
                    "','" + str(payload.get('price_amount')) + "',UTC_TIMESTAMP(), '"+str(status)+ \
                              "', '" + str(payload.get('payout_id')) + "',2)"
                    cur.execute(history)
                    cnx.commit()
                    if cur.rowcount > 0:
                        return {"Success": True, "data": payload.get('payout_id')}
                    else:
                        return {"Success": False, "data": "Данных нет"}
                else:
                    return {"Success": False, "data": "Заявка не найдена"}
            else:
                return {"Success": False, "data": "Заявка не создана, включите 2фа верификацию"}


# async def get_payment_status_by_uuid(payment_id):
#     with cpy.connect(**config.config) as cnx:
#         with cnx.cursor(dictionary=True) as cur:
#             string = "SELECT * FROM pay_history where payment_id = '" + str(payment_id) + "'"
#             cur.execute(string)
#             data = cur.fetchone()
#             if data:
#                 url = f"{config.base_url_np}payment/{payment_id}"
#                 headers = {
#                     "x-api-key": config.api_key_np,
#                     "Content-Type": "application/json"
#                 }
#                 response = requests.get(url, headers=headers)
#                 if response.status_code != 200:
#                     raise HTTPException(status_code=response.status_code, detail=response.json())
#                 print(response.json())
#                 return {"Success": True, "data": response.json()}
#             else:
#                 return {"Success": False, "data": "Данных нет"}


