import datetime

import mysql.connector as cpy
from fastapi import HTTPException

import config
from routers.actives.controller import crud_balance, crud_deposit
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
                docs_id = 0
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
                    #прикрепили ли платежку?
                    # string_find_doc = "SELECT id from pay_orders where uuid = '" + str(uuids) + "'"
                    # cur.execute(string_find_doc)

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
            #null_id = payload.get('id', -1)
            data_check = "select pay_orders.id, pay_orders.uuid, pay_orders.user_id, course, pay_orders.chart_id, " \
                         "chart.symbol as chart_symbol, sum_fiat, pay_pay.id as pay_id, " \
                         "pay_pay.title as pay_id_title, pay_orders.value, cashback, " \
                         "DATE_FORMAT(pay_orders.date, "+str(config.date_format_all)+") as date, " \
                         "DATE_FORMAT(pay_orders.date_expiry, "+str(config.date_format_all)+") as date_expiry, " \
                         "pay_reqs.id as pay_reqs_id, pay_reqs.uuid as pay_reqs_uuid, " \
                         "pay_reqs.phone, pay_reqs_types.title as pay_type, pay_notify_order_types_id, " \
                         "pay_fav_banks.id as bank_id, pay_fav_banks.title as banks_name, pay_fav_banks.bik, " \
                         "pay_notify_order_types.title as pay_notify_order_types_title, " \
                         "pay_docs.url as pay_docs_url " \
                         "from pay_orders " \
                         "LEFT JOIN chart ON pay_orders.chart_id = chart.id " \
                         "LEFT JOIN pay_pay ON pay_orders.pay_id = pay_pay.id " \
                         "LEFT JOIN pay_reqs ON pay_orders.req_id = pay_reqs.id " \
                         "LEFT JOIN pay_docs ON pay_orders.id = pay_docs.order_id " \
                         "LEFT JOIN pay_fav_banks ON pay_fav_banks.id = pay_reqs.bank_id " \
                         "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                         "LEFT JOIN pay_notify_order_types ON pay_orders.pay_notify_order_types_id = " \
                         "pay_notify_order_types.id " \
                         "where "
            # #if int(null_id) == 0:
            for k, v in dict(payload).items():
                if k != 'id':
                    if isinstance(v, list):
                        v = tuple(v)
                        data_check += "pay_orders." + str(k) + " in " + str(v) + " and "
                    else:
                        if k != 'date_start' and k != 'date_end':
                            data_check += "pay_orders." + str(k) + " = '" + str(v) + "' and "
            data_check += "pay_orders.id > 0"
            #фильтр по параметрам реквизитов

            # else:
            #     for k, v in dict(payload).items():
            #         if isinstance(v, list):
            #             v = tuple(v)
            #             data_check += "pay_orders." + str(k) + " in " + str(v) + " and "
            #         else:
            #             if k != 'date_start' and k != 'date_end':
            #                 data_check += "pay_orders." + str(k) + " = '" + str(v) + "' and "
            #     data_check += "pay_orders.id is not null"
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


async def update_order_by_any(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            #payin или payout
            check_pay = "select * from pay_orders where id = " + str(payload.get('id'))
            cur.execute(check_pay)
            data0 = cur.fetchone()
            if data0.get('pay_id') == 1:
                #проверяем PAYIN
                print(data0.get('pay_id'))
            elif data0.get('pay_id') == 2:
                # проверяем PAYOUT
                print(data0.get('pay_id'))
            else:
                return {"Success": False, "data": "Ордер не найден"}

            ###проверка по параметрам reqs
            ###всю логику блокировки баланса и депозита здесь###
            result = await block_baldep_by_status(data0, payload)
            if result["Success"]:
                data_update = "UPDATE pay_orders SET "
                for k, v in dict(payload).items():
                    if k != 'id':
                        data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where id = " + str(payload.get('id'))
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": str(result['data']) + ". Статус успешно изменен"}
                else:
                    return {"Success": False, "data": str(result['data']) + ". Статус не может быть изменен"}


async def delete_order_by_id(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 28 where id = " + str(id)
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
            #for i in images:
            string_check = "select * from pay_docs where order_id = " + str(order_id)
            cur.execute(string_check)
            data = cur.fetchall()
            if not data:
                insert_string = "INSERT into pay_docs (order_id, url) " \
                              "VALUES ('" + str(order_id) + "','" + str(images) + "')"
                cur.execute(insert_string)
                cnx.commit()
            else:
                update_string = "UPDATE pay_docs SET url = '" + str(images) + "' where order_id = " + str(order_id)
                cur.execute(update_string)
                cnx.commit()
            if cur.rowcount > 0:
                string_check = "select id from pay_docs where order_id = " + str(order_id)
                cur.execute(string_check)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data[0].get('id')}
                else:
                    return {"Success": False, "data": "Платежки не добавлены"}




async def get_docs_urls(order_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select * from pay_docs where order_id = " + str(order_id)
            cur.execute(data_check)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
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
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Статусы не получены"}


async def block_baldep_by_status(payload, new_status):
    """
    блокировка сумм от статуса ордера
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            new_status_notify = new_status.get('pay_notify_order_types_id')
            old_status_notify = payload.get('pay_notify_order_types_id')
            print(old_status_notify,new_status_notify)
            check_bal = "SELECT * FROM pay_balance where baldep_status_id = 1 and baldep_types_id = 1 and " \
                        "user_id = " + str(payload.get('user_id'))
            cur.execute(check_bal)
            value_bal = cur.fetchone()
            if value_bal:
                check_dep = "SELECT * FROM pay_deposit where baldep_status_id = 1 and baldep_types_id = 1 and " \
                            "user_id = " + str(payload.get('user_id'))
                cur.execute(check_dep)
                value_dep = cur.fetchone()
                if value_dep:
                    order_value = round(payload.get('value'),2)
                    # froze_bal = froze_dep = 0

                    get_bal = "select * from pay_balance where user_id = " + str(payload.get('user_id'))
                    cur.execute(get_bal)
                    bal_info = cur.fetchone()

                    payload_history = {
                        'user_id': payload.get('user_id'),
                        'balance_id': bal_info.get('id'),
                        'chart_id': payload.get('chart_id'),
                        'value': round(value_bal.get('value'), 2),
                        'frozen': order_value,
                        'balance_history_status_id': payload.get('id'),
                        'new_status_notify': new_status_notify
                        }

                    if order_value <= value_bal.get('value') + value_dep.get('value'):
                        if new_status_notify == 1:
                            print("принят ордер payin ждем оплаты, блокируем сумму с балдепозита", payload)
                            if order_value <= value_bal.get('value'):
                                froze_bal = order_value
                                result = await crud_balance("frozen", {'user_id': payload.get('user_id'), 'value': froze_bal})
                                if result["Success"]:
                                    result = await insert_balance_history(payload_history)
                                    if result["Success"]:
                                        return {"Success": True, "data": result['data'] + ". Сумма заблокирована"}
                                    else:
                                        return {"Success": False, "data": result['data'] + ". Сумма не заблокирована"}
                            else:
                                froze_bal = value_bal.get('value')
                                result = await crud_balance("frozen", {'user_id': payload.get('user_id'), 'value': froze_bal})
                                if result["Success"]:
                                    print("снимаем с депозита")
                                    if value_dep.get('value') >= order_value - value_bal.get('value'):
                                        froze_dep = order_value - value_bal.get('value')
                                        result = await crud_deposit("frozen", {'user_id': payload.get('user_id'), 'value': froze_dep})
                                        if result["Success"]:
                                            result = await insert_balance_history(payload_history)
                                            if result["Success"]:
                                                return {"Success": True, "data": result['data'] + ". Сумма "+str(order_value)+" USDT заблокирована"}
                                            else:
                                                return {"Success": False, "data": result['data'] + ". Сумма не заблокирована"}
                                        else:
                                            return {"Success": False, "data": result['data'] + ". История не обновилась"}
                                    else:
                                        return {"Success": False, "data": result['data'] + "Недостаточно баланса на депозите"}
                                else:
                                    return {"Success": False, "data": result['data'] + ". Сумма не заблокирована"}
                        elif new_status_notify == 2:
                            unfroze_sum = order_value
                            print(value_bal)
                            print(order_value, value_bal.get('frozen'))
                            if value_bal.get('frozen') >= unfroze_sum:
                                print("ордер отменен, разблокируем баланс по ордеру либо с баланса")
                                result = await crud_balance("unfrozen",
                                                            {'user_id': payload.get('user_id'), 'value': unfroze_sum})
                                if result["Success"]:
                                    result = await insert_balance_history(payload_history)
                                    if result["Success"]:
                                        # отправляем внутрянку USDT МЕРЧАНТУ
                                        return {"Success": True, "data": result['data'] + ". Сумма " + str(
                                            order_value) + " USDT разблокирована. Ордер отменен."}
                                    else:
                                        return {"Success": False, "data": result['data'] + ". Сумма не заблокирована"}
                                else:
                                    return {"Success": False, "data": result['data'] + ". Не удалось разморозить баланс. Обратитесь к администратору"}
                            else:
                                print("ордер отменен, разблокируем баланс по ордеру либо с баланса, либо частично баланс + депозит")
                                unfroze_sum_bal = value_bal.get('unfrozen')
                                unfroze_sum_dep = order_value - value_bal.get('frozen')
                                result = await crud_balance("unfrozen",
                                                            {'user_id': payload.get('user_id'), 'value': unfroze_sum_bal})
                                if result["Success"]:
                                    result = await crud_deposit("unfrozen",
                                                                {'user_id': payload.get('user_id'),
                                                                 'value': unfroze_sum_dep})
                                    if result["Success"]:
                                        result = await insert_balance_history(payload_history)
                                        if result["Success"]:
                                            return {"Success": True, "data": result['data'] + ". Сумма " + str(
                                                order_value) + " USDT разблокирована"}
                                        else:
                                            return {"Success": False,
                                                    "data": result['data'] + ". Сумма не разблокирована"}
                                    else:
                                        return {"Success": False, "data": result[
                                                                              'data'] + ". Не удалось разморозить депозит. Обратитесь к администратору"}
                                else:
                                    return {"Success": False, "data": result[
                                                                          'data'] + ". Не удалось разморозить баланс. Обратитесь к администратору"}
                        elif new_status_notify == 3:
                            print("ордер успешный PAYIN, отправили USDT на баланс мерчанту")
                            # то есть 2 + внутренний перевод
                        elif new_status_notify == 4:
                            print("ордер оплачен, время еще не вышло но не сработала автоматика")







                        else:
                            return {"Success": True, "data": "тест. статус изменен"}
                    else:
                        return {"Success": False, "data": "Не достаточно средств. Обратитесь к администратору"}
                else:
                    return {"Success": False,
                            "data": "Не возможно выполнить операции с депозитом"}
            else:
                return {"Success": False,
                        "data": "Не возможно выполнить операции с балансом"}


async def insert_balance_history(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            insert_string = "INSERT into pay_balance_history (user_id, balance_id, chart_id, " \
                            "date, value, frozen, balance_history_status_id, " \
                            "description, order_id) VALUES ('" + str(payload.get('user_id')) \
                            + "','" + str(payload.get('balance_id')) + "','"+str(payload.get('chart_id')) \
                            + "',UTC_TIMESTAMP(), '" \
                            + str(round(payload.get('value'), 2)) + "','" + str(payload.get('frozen')) \
                            + "','" + str(payload.get('new_status_notify')) + "','блокировка','" \
                            + str(payload.get('balance_history_status_id')) + "')"
            print(insert_string)
            cur.execute(insert_string)

            cnx.commit()
            if cur.rowcount > 0:
                return {"Success": True, "data": "История баланса обновлена"}
            else:
                return {"Success": False, "data": "Не удалось записать историю баланса"}