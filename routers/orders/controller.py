import datetime

import mysql.connector as cpy
from fastapi import HTTPException

import config
from routers.orders.utils import generate_uuid
import requests
import telebot

botgreenavipay = telebot.TeleBot(config.telegram_api)


async def get_course():

    api_url = "https://api.coinbase.com/v2/prices/USDT-RUB/spot"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


async def create_order_for_user(payload):
    with (cpy.connect(**config.config) as cnx):
        with cnx.cursor(dictionary=True) as cur:
            uuids = await generate_uuid()
            string0 = "SELECT * FROM pay_reqs WHERE pay_pay_id = '" + str(payload.get('pay_id')) \
            + "' and id = " + str(payload.get('req_id'))
            cur.execute(string0)
            data = cur.fetchone()
            if data:
                string_cash = "SELECT value from pay_pay_percent where pay_id = '"+str(payload.get('pay_id'))+"' " \
                              "and pay_status_id = 1 and user_id = " + str(data['user_id']) #payin / payout
                cur.execute(string_cash)
                cashback = cur.fetchone()
                print(cashback)
                if not cashback:
                    return {"Success": False, "data": "Не установлен процент cashback, обратитесь к администратору"}
                course = await get_course()
                cashback_value = float(cashback.get('value',1))
                print(cashback_value)
                course2 = float(course['data']['amount']) * (1 + cashback_value / 100)
                #course2 = float(course) * (1 + cashback / 100) #test
                currency_id = 1 #todo из sms_data
                docs_id = 1 # todo из docs после фото документа
                summ = float(payload.get('sum_fiat')) / course2
                if int(payload.get('pay_id')) == 1:
                    interval_order = config.TIME_ORDER_PAYIN_EXPIRY
                else:
                    interval_order = config.TIME_ORDER_PAYOUT_EXPIRY
                data_string = "INSERT INTO pay_orders (uuid, user_id, course, chart_id, sum_fiat, pay_id," \
                              "value, cashback, date, date_expiry, req_id, pay_notify_order_types_id, docs_id) " \
                              "VALUES ('" + str(uuids) + "','" + str(data['user_id']) + \
                              "','" + str(round(course2,2)) + "','" + str(currency_id) + "','" + \
                              str(payload.get('sum_fiat')) + "','"+str(payload.get('pay_id'))\
                              + "','" + str(round(summ, 2)) + "','" \
                              + str(cashback_value) + "',UTC_TIMESTAMP(), DATE_ADD(UTC_TIMESTAMP(), INTERVAL " + str(interval_order) + " minute ),'" \
                              + str(data['id']) + "',0,'" + str(docs_id) + "')"
                print(data_string)
                cur.execute(data_string)
                cnx.commit()
                if cur.rowcount > 0:
                    message = "Ордер " + str(uuids) + " \nпоставлен в очередь со статусом СОЗДАН, \n"\
                              + str(datetime.datetime.now()) + "\nна сумму: " + str(payload.get('sum_fiat')) + " руб."
                    botgreenavipay.send_message(config.pay_main_group, message, parse_mode='HTML')
                    return {"Success": True, "data": "Ордер поставлен в очередь. Ожидайте исполнения"}
                else:
                    return {"Success": False, "data": "Ордер не может быть создан"}
            else:
                return {"Success": False, "data": "Реквизиты не найдены или отключены"}


async def get_orders_by_any(payload):
    """
    фильтр по указанным параметрам
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            null_id = payload.get('id', -1)
            data_check = "select pay_orders.id, pay_orders.uuid, pay_orders.user_id, course, pay_orders.chart_id, " \
                         "chart.symbol as chart_symbol, sum_fiat, pay_pay.id as pay_id, " \
                         "pay_pay.title as pay_id_title, pay_orders.value, cashback, " \
                         "pay_orders.date, date_expiry, pay_reqs.id as pay_reqs_id, pay_reqs.uuid as pay_reqs_uuid, " \
                         "pay_reqs.phone, pay_reqs_types.title as pay_type, pay_notify_order_types_id, " \
                         "pay_fav_banks.id as bank_id, pay_fav_banks.title as banks_name, pay_fav_banks.bik, " \
                         "pay_notify_order_types.title as pay_notify_order_types_title, " \
                         "pay_docs.url as pay_docs_url " \
                         "from pay_orders " \
                         "LEFT JOIN chart ON pay_orders.chart_id = chart.id " \
                         "LEFT JOIN pay_pay ON pay_orders.pay_id = pay_pay.id " \
                         "LEFT JOIN pay_reqs ON pay_orders.req_id = pay_reqs.id " \
                         "LEFT JOIN pay_docs ON pay_orders.docs_id = pay_docs.order_id " \
                         "LEFT JOIN pay_fav_banks ON pay_fav_banks.id = pay_reqs.bank_id " \
                         "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                         "LEFT JOIN pay_notify_order_types ON pay_orders.pay_notify_order_types_id = " \
                         "pay_notify_order_types.id " \
                         "where "
            if int(null_id) == 0:
                for k, v in dict(payload).items():
                    if k != 'id':
                        if isinstance(v, list):
                            v = tuple(v)
                            data_check += "pay_orders." + str(k) + " in " + str(v) + " and "
                        else:
                            if k != 'date_start' and k != 'date_end':
                                data_check += "pay_orders." + str(k) + " = '" + str(v) + "' and "
                data_check += "pay_orders.id > 0"
            else:
                for k, v in dict(payload).items():
                    if isinstance(v, list):
                        v = tuple(v)
                        data_check += "pay_orders." + str(k) + " in " + str(v) + " and "
                    else:
                        if k != 'date_start' and k != 'date_end':
                            data_check += "pay_orders." + str(k) + " = '" + str(v) + "' and "
                data_check += "pay_orders.id is not null"
            # try: #todo эталон фильтр по датам
            #     if payload['date_start'] is not None and payload['date_end'] is not None:
            #         data_check += " and pay_orders.date >= '" + str(payload['date_start']) \
            #                   + " 00:00' and pay_orders.date <= '" + str(payload['date_end']) + " 23:59'"
            # except:
            #     print("фильтр по датам не выбран")
            print(data_check)
            cur.execute(data_check)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Ордера не найдены"}


async def update_order_by_id(id, pay_notify_order_types_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # def check_status

            string = "UPDATE pay_orders SET pay_notify_order_types_id = '" \
                     "" + str(pay_notify_order_types_id) + \
                     "' where id = " + str(id)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                return {"Success": True, "data": "Статус успешно изменен"}
            else:
                return {"Success": False, "data": "Статус не может быть изменен"}


async def delete_order_by_id(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 26 where id = " + str(id)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно изменен"}
            else:
                cnx.close()
                return {"Success": False, "data": "Статус не может быть изменен"}


async def insert_docs(order_id, images):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            try:
                for i in images:
                    data_string = "INSERT into docs (order_id, url) " \
                                  "VALUES ('" + str(order_id) + "','" + str(i) + "')"
                    cur.execute(data_string)
                    cnx.commit()
                cnx.close()
                return {"Success": True, "data": "Документы добавлены"}
            except:
                return {"Success": False, "data": "Платежки не добавлены"}


async def get_docs_urls(order_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select * from pay_docs where order_id = " + str(order_id)
            cur.execute(data_check)
            check = cur.fetchall()
            if check:
                cnx.close()
                return {"Success": True, "data": check}
            else:
                cnx.close()
                return {"Success": False, "data": "Платежки не найдены"}


async def create_new_cashback_for_group(payload):
    print(payload)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_string = "INSERT INTO pay_cashback (title, date, pay_reqs_group_id, value, status_id) " \
                          "VALUES ('" + str(payload['title']) + "', NOW(), '" + str(payload['pay_reqs_group_id']) \
                          + "','" + str(payload['value']) + "','" + str(payload['status_id']) + "')"
            cur.execute(data_string)
            try:
                cnx.commit()
                cnx.close()
                return {"Success": True, "data": "Кешбек добавлен"}
            except:
                cnx.close()
                return {"Success": False, "data": "Кешбек не добавлен"}


async def set_cashback_to_group(id, value):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_string = "UPDATE cashback SET value = " + str(value) + " where id = " + str(id)
            cur.execute(data_string)
            try:
                cnx.commit()
                cnx.close()
                return {"Success": True, "data": "Кешбек обновлен"}
            except:
                cnx.close()
                return {"Success": False, "data": "Кешбек не добавлен"}


async def set_cashback_status_for_group_by_id(id, value):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_string = "UPDATE pay_cashback SET status_id = " + str(value) + " where id = " + str(id)
            cur.execute(data_string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Статус кешбека обновлен"}
            else:
                cnx.close()
                return {"Success": False, "data": "Статус кешбека не обновлен"}


async def get_all_cashback_statuses(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_string = "SELECT * from pay_cashback_status"
            cur.execute(data_string)
            data = cur.fetchall()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                cnx.close()
                return {"Success": False, "data": "Статусы не получены"}


async def get_all_cashback_by_id(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_string = "SELECT pay_cashback.title, pay_cashback.date, reqs_group_id, " \
                          "pay_reqs_groups.title as reqs_group_title, value, status_id,  " \
                          "pay_cashback_status.title as status_title " \
                          "from pay_cashback " \
                          "LEFT JOIN pay_cashback_status ON pay_cashback.status_id = pay_cashback_status.id " \
                          "LEFT JOIN pay_reqs_groups ON pay_reqs_groups.id = pay_cashback.reqs_group_id "
            cur.execute(data_string)
            data = cur.fetchall()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                cnx.close()
                return {"Success": False, "data": "Статусы не получены"}
