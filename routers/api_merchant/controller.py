import mysql.connector as cpy
import config
from routers.admin.utils import create_random_key
from routers.orders.utils import generate_uuid


async def get_settings(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if user_id == 0:
                check_settings = "SELECT * FROM pay_notify_user_settings"
                cur.execute(check_settings)
                data = cur.fetchall()
            else:
                check_settings = "SELECT * FROM pay_notify_user_settings where user_id = '" + str(user_id) + "'"
                cur.execute(check_settings)
                data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось найти параметры"}


async def set_settings(payload):
    with (cpy.connect(**config.config) as cnx):
        with cnx.cursor(dictionary=True) as cur:

            check_settings = "SELECT * FROM pay_notify_user_settings where user_id = '" + str(payload.get('user_id')) + "'"
            cur.execute(check_settings)
            data = cur.fetchone()
            if data:
                data_update = "UPDATE pay_notify_user_settings SET "
                for k, v in dict(payload).items():
                    if k != 'user_id':
                        data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where user_id = " + str(payload.get('user_id'))
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно обновлены настройки мерчанта"}
                else:
                    return {"Success": False, "data": "настройки мерчанта не обновлены"}
            else:
                secret_word = await create_random_key(20)
                data_insert = "INSERT into pay_notify_user_settings (user_id, site_url, success_url, " \
                               "fail_url, secret_word) VALUES (" \
                + str(payload.get('user_id')) + ", '" + str(payload.get('site_url')) + "', '" + str(payload.get('success_url')) \
                + "', '" + str(payload.get('fail_url')) + "', '" + str(secret_word) + "')"
                print(data_insert)
                cur.execute(data_insert)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно обновлены настройки"}
                else:
                    return {"Success": False, "data": "настройки не обновлены"}


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
                data_insert = "INSERT into pay_shops (uuid, user_id, title, balance, date " \
                              ") VALUES ('" \
                              + str(uuids) + "', '" + str(payload.get('user_id')) + "', '" + str(
                                payload.get('title')) + "', 0, UTC_TIMESTAMP())"
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
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось найти магазин"}