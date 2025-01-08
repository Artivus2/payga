import mysql.connector as cpy
import config
from routers.admin.utils import create_random_key


async def get_settings(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if user_id == 0:
                print(user_id)
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
                    return {"Success": True, "data": "Успешно обновлены реквизиты группы"}
                else:
                    return {"Success": False, "data": "реквизиты группы не обновлены"}
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
