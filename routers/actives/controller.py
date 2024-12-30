import datetime

import mysql.connector as cpy
import config


async def crud_balance_percent(crud, payload):  # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """
    print(payload)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                string0 = "SELECT * FROM pay_pay_percent where user_id = " + str(payload.user_id) + \
                          " and pay_id = " + str(payload.pay_id)
                cur.execute(string0)
                data0 = cur.fetchall()
                if not data0:
                    data_str = "INSERT INTO pay_pay_percent (user_id, pay_id, value, date, pay_status_id) " \
                               "VALUES ('" + str(payload.user_id) + "','" + str(payload.pay_id) + "','" \
                               + str(payload.value) + "', UTC_TIMESTAMP() , 1)"
                    cur.execute(data_str)
                    cnx.commit()
                    if cur.rowcount > 0:
                        return {"Success": True, "data": "Операция проведена"}
                    else:
                        return {"Success": False, "data": "Операцию провести не удалось"}
                else:
                    return {"Success": False, "data": "Уже есть процент по данному пользователю"}

            if crud == 'get':
                string = "select user_id, pay_id, pay_pay.title as pay_title, " \
                         "value, DATE_FORMAT(date, " + str(config.date_format_all) + ") as date, " \
                         "pay_status_id, pay_pay_status.title as pay_status_title " \
                         "from pay_pay_percent " \
                         "LEFT JOIN pay_pay ON pay_pay_percent.pay_id = pay_pay.id " \
                         "LEFT JOIN pay_pay_status ON pay_pay_percent.pay_status_id = pay_pay_status.id "
                if int(payload.user_id) == 0:  # todo left join
                    dop = ""
                else:
                    dop = "where pay_id = "+str(payload.pay_id)+" and user_id = " + str(payload.user_id)
                string += dop
                cur.execute(string)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}
            if crud == 'set':

                string = "UPDATE pay_pay_percent SET value = '" + str(
                    payload.value) + "', pay_status_id = 1 where user_id = " + str(
                    payload.user_id) + " and pay_id = " + str(payload.pay_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно изменен"}
                else:
                    return {"Success": False, "data": "Не удалось изменить"}
            if crud == 'remove':
                string = "DELETE FROM pay_pay_percent " \
                         "where user_id = " + str(payload.user_id) + " and pay_id = " + str(payload.pay_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно удален"}
                else:
                    return {"Success": False, "data": "Не удалось удалить"}
            cnx.close()


async def crud_balance(crud, payload):  # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """

    with (cpy.connect(**config.config) as cnx):
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                # todo проверить есть уже баланс insert or update
                data_string = "INSERT INTO pay_balance (user_id, value, chart_id, baldep_status_id, " \
                              "baldep_types_id, date, frozen, withdrawals) " \
                              "VALUES ('" + str(payload.user_id) + "',0,259,1,1,UTC_TIMESTAMP(), 0, 0)"

                cur.execute(data_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Баланс пользователя создан"}
                else:
                    return {"Success": False, "data": "Баланс не может быть создан"}
            if crud == 'get':
                if int(payload) == 0:  # todo left join
                    string = "select * from pay_balance"
                else:
                    string = "select user_id, value, chart_id, baldep_status_id, baldep_types_id, frozen, withdrawals, " \
                             "chart.symbol as chart_symbol, pay_baldep_types.title as pay_baldep_types_title, " \
                             "pay_baldep_status.title as pay_baldep_status_title " \
                             "from pay_balance " \
                             "LEFT JOIN chart ON pay_balance.chart_id = chart.id " \
                             "LEFT JOIN pay_baldep_types ON pay_balance.baldep_types_id = pay_baldep_types.id " \
                             "LEFT JOIN pay_baldep_status ON pay_balance.baldep_status_id = pay_baldep_status.id " \
                             "where user_id = " + str(payload)
                cur.execute(string)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}
            if crud == 'set':
                data_update = "UPDATE pay_balance SET "
                payload2 = {}
                for k, v in dict(payload).items():
                    if v is not None:
                        payload2[k] = v
                        if k != 'user_id':
                            data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where user_id = " + str(payload.user_id)
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно изменен"}
                else:
                    return {"Success": False, "data": "Не удалось изменить баланс"}

            if crud == 'remove':
                string = "DELETE from pay_balance " \
                         "where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                cnx.close()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно удален"}
                else:
                    return {"Success": False, "data": "Не удалось удалить баланс"}
            if crud == 'status':
                string = "UPDATE pay_balance set baldep_status_id = '" + str(payload.baldep_status_id) \
                         + "' where user_id = " + str(payload.user_id)
                cur.execute(string)
                try:
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Статус изменен"}
                except:
                    return {"Success": False, "data": "Не удалось имзенить статус"}
            if crud == 'type':
                string = "UPDATE pay_balance set baldep_types_id = '" \
                         + str(payload.baldep_types_id) + "' where user_id = " + str(payload.user_id)
                cur.execute(string)
                try:
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Тип изменен"}
                except:
                    return {"Success": False, "data": "Не удалось имзенить тип"}
            #withdrawals
            if crud == 'withdrawals':
                string0 = "SELECT value, withdrawals FROM pay_balance where user_id = " + str(payload.user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                current_value = float(data0.get('value', 0))
                current_withdrawals = float(data0.get('withdrawals', 0))
                if current_withdrawals == 0:
                    if current_value >= payload.value:
                        string = "UPDATE pay_balance set value = '" + str(current_value - payload.value) + \
                                 "', withdrawals = '" + str(current_withdrawals + payload.value) + \
                                 "' where user_id = " + str(payload.user_id)
                        cur.execute(string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            # история выводов

                            # вывести в сеть
                            return {"Success": True, "data": "Cредства отправлены на вывод"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить доступные средства баланса"}
                    else:
                        return {"Success": False, "data": "Недостаточно средств на балансе"}
                else:
                    return {"Success": False, "data": "У вас уже есть необработанные заявки на вывод"}

            if crud == 'frozen':

                user_id = payload.get('user_id')
                value = float(payload.get('value'))
                string0 = "SELECT value, frozen FROM pay_balance where user_id = " + str(user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                if data0:

                    current_value = float(data0.get('value', 0))
                    current_frozen = float(data0.get('frozen', 0))
                    if current_value > value:
                        string = "UPDATE pay_balance set value = '" + str(current_value - value) + \
                                 "', frozen = '" + str(current_frozen + value) + \
                                 "' where user_id = " + str(user_id)
                        cur.execute(string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True, "data": "Средства баланса заморожены: " + str(value) + " USDT"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить доступные средства баланса"}
                    else:
                        return {"Success": False, "data": "Недостаточно средств на балансе"}
                else:
                    return {"Success": False, "data": "Отсутствует информация о балансе отправителя"}
            if crud == 'unfrozen':
                user_id = payload.get('user_id')
                value = float(payload.get('value'))
                string0 = "SELECT value, frozen FROM pay_balance where user_id = " + str(user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                current_value = float(data0.get('value', 0))
                current_frozen = float(data0.get('frozen', 0))
                if current_frozen == 0:
                    if current_frozen > value:
                        string = "UPDATE pay_balance set value = '" + str(current_value + value) + \
                                 "', frozen = '" + str(current_frozen - value) + \
                                 "' where user_id = " + str(user_id)
                        cur.execute(string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True,
                                    "data": "Средства баланса разморожены: " + str(value) + " USDT"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить frozen средства"}
                    else:
                        return {"Success": False, "data": "Недостаточно средств на заморозке"}
                else:
                    return {"Success": False, "data": "У вас уже есть необработанные заявки на вывод"}


async def get_balance_history_historyes(user_id=0):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT pay_balance_history.id, user_id, chart_id, chart.symbol as chart_symbol, value, frozen, " \
                     "DATE_FORMAT(date, " + str(config.date_format_all) + ") as date, " \
                      "balance_history_status_id, " \
                      "pay_balance_history_status.title as balance_history_status_title, description " \
                      "from pay_balance_history " \
                      "LEFT JOIN pay_balance_history_status ON " \
                      "pay_balance_history_status.id = pay_balance_history.balance_history_status_id " \
                      "LEFT JOIN chart ON pay_balance_history.chart_id = chart.id "
            if user_id != 0:
                string += "where user_id = " + str(user_id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def get_balance_history_statuses():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "select id, title from pay_balance_history_status "
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def get_deposit_history_statuses():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "select id, title from pay_deposit_history_status "
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}

async def check_min_deposit(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT min_deposit from pay_deposit where user_id = " + str(payload.user_id)
            cur.execute(check_string)
            data = cur.fetchone()
            if not data:
                return {"Success": False, "data": "Ну установлены параметры инимального депозита"}
            else:
                return {"Success": True}


async def check_deposit_status(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT baldep_status_id from pay_deposit where baldep_status_id = 1 " \
                           "and user_id = " + str(payload.user_id)
            cur.execute(check_string)
            data = cur.fetchone()
            if not data:
                return {"Success": False, "data": "Статус депозита не подтвержден. Обратитесь к администратору"}
            else:
                return {"Success": True}


async def check_deposit_type(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT baldep_types_id from pay_deposit where baldep_types_id = 1 " \
                           "and user_id = " + str(payload.user_id)
            cur.execute(check_string)
            data = cur.fetchone()
            if not data:
                return {"Success": False, "data": "Тип депозита не определен. Обратитесь к администратору"}
            else:
                return {"Success": True}


async def crud_deposit(crud, payload):  # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                check_deposit = "SELECT * from pay_deposit where user_id = " + str(payload.user_id)
                cur.execute(check_deposit)
                data = cur.fetchone()
                if not data:
                    data_string = "INSERT INTO pay_deposit (user_id, value, baldep_status_id, " \
                                  "baldep_types_id, frozen, date, min_deposit) " \
                                  "VALUES ('" + str(payload.user_id) + "',0,1,1,0,UTC_TIMESTAMP(),0)"
                    cur.execute(data_string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        return {"Success": True, "data": "Аккаунт депозита создан"}
                    else:
                        return {"Success": False, "data": "Депозит не может быть создан"}
                else:
                    return {"Success": False, "data": "Депозит уже существует, обратитесь к адинистратору"}

            if crud == 'get':
                if int(payload) == 0:
                    string = "select * from pay_deposit"
                else:
                    string = "select user_id, value, baldep_status_id, baldep_types_id, " \
                             "pay_baldep_types.title as pay_baldep_types_title, " \
                             "pay_baldep_status.title as pay_baldep_status_title, frozen, min_deposit, date, withdrawals " \
                             "from pay_deposit " \
                             "LEFT JOIN pay_baldep_types ON pay_deposit.baldep_types_id = pay_baldep_types.id " \
                             "LEFT JOIN pay_baldep_status ON pay_deposit.baldep_status_id = pay_baldep_status.id " \
                             "where user_id = " + str(payload)
                cur.execute(string)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}
            if crud == 'set':
                check_min = await check_min_deposit(payload)
                if check_min["Success"]:
                    string = "UPDATE pay_deposit set value = '" + str(payload.value) + \
                             "' where user_id = " + str(payload.user_id)
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        cnx.close()
                        return {"Success": True, "data": "Успешно изменен"}
                    else:
                        cnx.close()
                        return {"Success": False, "data": "Не удалось изменить депозит"}
                else:
                    return {"Success": False, "data": "Не удалось изменить депозит"}
            #set min deposit
            if crud == 'set-min':
                check_type = await check_deposit_type(payload)
                check_status = await check_deposit_status(payload)
                if check_type["Success"]:
                    if check_status["Success"]:
                        string = "UPDATE pay_deposit set min_deposit = '" + str(payload.value) + \
                                 "' where user_id = " + str(payload.user_id)
                        cur.execute(string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True, "data": "Минимальный депозит изменен"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить депозит"}
                    else:
                        return {"Success": False, "data": "Не удалось изменить депозит"}
                else:
                    return {"Success": False, "data": "Не удалось изменить депозит"}

            if crud == 'remove':
                string = "DELETE from pay_deposit " \
                         "where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                cnx.close()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно удален"}
                else:
                    return {"Success": False, "data": "Не удалось удалить депозит"}
            if crud == 'status':
                string = "UPDATE pay_deposit set baldep_status_id = '" + str(payload.baldep_status_id) \
                         + "' where user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Статус изменен"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Не удалось имзенить статус"}
            if crud == 'type':
                string = "UPDATE pay_deposit SET baldep_types_id = '" + str(payload.baldep_types_id) + "' " \
                         "where user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Тип изменен"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Не удалось изменить тип"}
            if crud == 'frozen':
                string0 = "SELECT value, frozen FROM pay_deposit where baldep_status_id = 1 and " \
                                          "baldep_types_id = 1 and user_id = " + str(payload.user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                if data0:
                    current_value = float(data0.get('value')) #value получаем
                    current_frozen = float(data0.get('frozen'))
                    if payload.value is None:
                        payload.value = 0
                    if payload.frozen is None:
                        payload.frozen = 0
                    if current_frozen == 0:
                        if current_value > 0 and current_value >= payload.frozen and (current_frozen + payload.frozen) >= 0:
                            string = "UPDATE pay_deposit set value = '" + str(current_value - payload.value) + \
                                     "', frozen = '" + str(current_frozen + payload.value) + \
                                     "' where user_id = " + str(payload.user_id)

                            cur.execute(string)
                            cnx.commit()
                            cnx.close()
                            if cur.rowcount > 0:
                                return {"Success": True, "data": "Изменены доступные средства депозита"}
                            else:
                                return {"Success": False, "data": "Не удалось изменить доступные средства депозита"}
                        else:
                            return {"Success": False, "data": "Недостаточно средств депозита"}
                    else:
                        return {"Success": False, "data": "У вас уже есть необработанные заявки на вывод"}
                else:
                    return {"Success": False, "data": "Депозит не найден или заблокирован"}
            if crud == 'unfrozen':
                string0 = "SELECT value, frozen FROM pay_deposit where baldep_status_id = 1 and " \
                                          "baldep_types_id = 1 and user_id = " + str(payload.user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                print(data0)
                if data0:
                    current_value = float(data0.get('value'))
                    current_frozen = float(data0.get('frozen'))
                    if payload.value is None:
                        payload.value = 0
                    if payload.frozen is None:
                        payload.frozen = 0

                    if current_value >= 0 and current_frozen >= 0 and current_frozen - payload.frozen >= 0:
                        string = "UPDATE pay_deposit set value = '" + str(current_value + payload.frozen) + \
                                 "', frozen = '" + str(current_frozen - payload.frozen) + \
                                 "' where user_id = " + str(payload.user_id)
                        cur.execute(string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True, "data": "Изменены доступные средства депозита"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить доступные средства депозита"}
                    else:
                        return {"Success": False, "data": "Недостаточно средств депозита"}
                else:
                    return {"Success": False, "data": "Депозит не найден или заблокирован"}
            if crud == 'withdrawals':
                string0 = "SELECT value, withdrawals FROM pay_deposit where baldep_status_id = 1 and " \
                          "baldep_types_id = 1 and user_id = " + str(payload.user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                if data0:
                    current_value = float(data0.get('value'))  # value получаем
                    current_withdrawals = float(data0.get('withdrawals'))
                    if payload.value is None:
                        payload.value = 0
                    if current_withdrawals == 0:
                        if current_value >= current_withdrawals:
                            string = "UPDATE pay_deposit set value = '" + str(round(current_value - payload.value, 2)) + \
                                     "', withdrawals = '" + str(round(current_withdrawals + payload.value, 2)) + \
                                     "' where user_id = " + str(payload.user_id)
                            cur.execute(string)
                            cnx.commit()
                            if cur.rowcount > 0:
                                return {"Success": True,
                                        "data": "Заявка на вывод средств с депозита одобрена. Ожидайте подтверждения."}
                            else:
                                return {"Success": False, "data": "Не удалось изменить доступные средства депозита"}
                        else:
                            return {"Success": False, "data": "Недостаточно средств депозита"}
                    else:
                        return {"Success": False, "data": "У вас уже есть необработанные заявки на вывод"}
                else:
                    return {"Success": False, "data": "Депозит не найден или заблокирован"}


async def dep_withdrawal_check(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            history_check = "select * from pay_deposit_history where status_id in (0,6) " \
                            "and user_id = " + str(payload.user_id)
            cur.execute(history_check)
            data0 = cur.fetchall()
            if not data0:
                date_check_from_balance = "SELECT date FROM pay_balance_history where " \
                                          "user_id = '" + str(payload.user_id) + "' and " \
                                          "date < DATE_ADD(UTC_TIMESTAMP(), INTERVAL -1 month)"
                cur.execute(date_check_from_balance)
                data = cur.fetchall()
                if data:
                    return {"Success": False, "data": "Вы не можете выводить с депозита не прошел срок 1 месяц"}
                else:
                    result = await crud_deposit("withdrawals", payload)
                    if result["Success"]:
                        insert_string = "INSERT into pay_deposit_history (user_id, date, " \
                                        "balordep, value, status_id) VALUES ('" + str(payload.user_id) \
                                        + "', UTC_TIMESTAMP(), 1, '" + str(payload.value) + "',0)"
                        cur.execute(insert_string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True, "data":
                                result["data"] + ". Вывод с депозита будет подтвержден администратором. Ожидайте."}
                        else:
                            return {"Success": False, "data":
                                result["data"] + ". Вывод не может быть осуществлен. Обратитесь к администратору"}
                    return {"Success": False, "data":
                        result["data"] + ". Вывод не может быть осуществлен. Обратитесь к администратору"}
            else:
                return {"Success": False, "data": "Есть не обработаные заявки на вывод. Обратитесь к администратору"}




async def bal_withdrawal_check(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            history_check = "select * from pay_deposit_history where status_id in (0,6) " \
                            "and user_id = " + str(payload.user_id)
            cur.execute(history_check)
            data0 = cur.fetchall()
            if not data0:
                check_string = "SELECT value, withdrawals FROM pay_balance where baldep_status_id = 1" \
                               " and baldep_types_id = 1 and " \
                               "value > 0 and withdrawals = 0 and user_id = " + str(payload.user_id)
                cur.execute(check_string)
                data = cur.fetchone()
                if data:
                    #переводим с value на withdrawals
                    result = await crud_balance("withdrawals", payload)
                    if result["Success"]:
                        insert_string = "INSERT into pay_deposit_history (user_id, date, " \
                                        "balordep, value, status_id) VALUES ('" + str(payload.user_id) + "', " \
                                        + "UTC_TIMESTAMP(), 2, '" + str(payload.value) + "',0)"
                        cur.execute(insert_string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True, "data": result['data'] + ". Ожидайте подтверждения администратором."}
                        else:
                            return {"Success": False, "data": result['data'] + ". Не выполнено."}
                    else:
                        return {"Success": False, "data": result['data'] + ". Операция не выполнена."}
                else:
                    return {"Success": False, "data": "Есть не обработаные остатки на счету для вывода. Обратитесь к администратору"}
            else:
                return {"Success": False, "data": "Есть не обработаные заявки на вывод. Обратитесь к администратору"}



async def bal_refunds_check(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            print(payload)
            bal_check = "select * from pay_balance where user_id = " + str(payload.user_id)
            cur.execute(bal_check)
            data_bal = cur.fetchone()
            if data_bal:
                dep_check = "select * from pay_deposit where min_deposit > 0 and user_id = " + str(payload.user_id)
                cur.execute(dep_check)
                data_dep = cur.fetchone()
                if data_dep:
                    history_check = "select * from pay_deposit_history where status_id in (0,6) " \
                                    "and user_id = " + str(payload.user_id)
                    cur.execute(history_check)
                    data0 = cur.fetchall()
                    if not data0:
                        check_string = "SELECT value FROM pay_balance where baldep_status_id = 1" \
                                       " and baldep_types_id = 1 and " \
                                       "user_id = " + str(payload.user_id)
                        cur.execute(check_string)
                        data = cur.fetchone()
                        if data:
                            # запоминаем сумму ввода в истории
                            insert_string = "INSERT into pay_deposit_history (user_id, date, " \
                                            "balordep, value, status_id) VALUES ('" + str(payload.user_id) + "', " \
                                            + "UTC_TIMESTAMP(), 2, '" + str(payload.value) + "',6)"
                            cur.execute(insert_string)
                            cnx.commit()
                            if cur.rowcount > 0:
                                return {"Success": True,
                                        "data": "Ожидайте подтверждение пополенения администратором."}
                            else:
                                return {"Success": False, "data": "Не удалось создать заявку на ввод средств"}
                        else:
                            return {"Success": False, "data": "Операция не может быть выполнена"}
                    else:
                        return {"Success": False, "data": "У вас есть не обработанные заявки на ввод / вывод"}
                else:
                    return {"Success": False, "data": "Не установлен лимит депозита. Обратитесь к администратрору"}
            else:
                return {"Success": False, "data": "Баланс не найден. Обратитесь к администратрору"}




async def get_pay_type_by_id(id):
    """
    :param status_id:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                string = "select id, title from pay_pay"
            else:
                string = "select id, title from pay_pay " \
                         "where id = " + str(id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def get_pay_status_by_id(id):
    """
    :param status_id:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                string = "select id, title from pay_pay_status"
            else:
                string = "select id, title from pay_pay_status " \
                         "where id = " + str(id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def get_baldep_status_by_id(id):
    """
    :param status_id:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                string = "select id, title from pay_baldep_status"
            else:
                string = "select id, title from pay_baldep_status " \
                         "where id = " + str(id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def get_baldep_types_by_id(id):
    """
    :param status_id:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                string = "select id, title from pay_baldep_types"
            else:
                string = "select id, title from pay_baldep_types " \
                         "where id = " + str(id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def get_transfer_status_by_id(status_id):
    """

    :param status_id:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(status_id) == 0:
                string = "select id, title from pay_transfer_status"
            else:
                string = "select id, title from pay_transfer_status " \
                         "where id = " + str(status_id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "не удалось выполнить операцию"}


async def crud_wallet(crud, payload):  # todo -> admin
    """
    user_id: int
    network: str
    address: str
    wallet_status_id: int
    date: int
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_string = "INSERT INTO pay_wallet (user_id, network, address, wallet_status_id, date) " \
                              "VALUES ('" + str(payload.user_id) + "','" + str(payload.network) + \
                              "','" + str(payload.address) + "','1', NOW())"
                try:
                    cur.execute(data_string)
                    cnx.commit()
                    return {"Success": True, "data": "Кошелек пользователя создан"}
                except:
                    return {"Success": False, "data": "Кошелек не может быть создан"}
            if crud == 'get':
                if int(payload.user_id) == 0:
                    string = "select user_id, network, address, wallet_status_id, pay_wallet_status.title " \
                             "from pay_wallet " \
                             "LEFT JOIN pay_wallet_status ON pay_wallet.wallet_status_id = pay_wallet_status.id "
                else:
                    string = "select user_id, network, address, wallet_status_id, pay_wallet_status.title " \
                             "from pay_wallet " \
                             "LEFT JOIN pay_wallet_status ON pay_wallet.wallet_status_id = pay_wallet_status.id " \
                             "where user_id = " + str(payload.user_id)
                cur.execute(string)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}

            if crud == 'set':
                string = "UPDATE pay_wallet set wallet_status_id = '" + str(payload.wallet_status_id) + \
                         "' where user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно изменен"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Не удалось изменить статус кошелька"}
            if crud == 'remove':
                string = "DELETE from pay_wallet  " \
                         "where user_id = " + str(payload.user_id)
                cur.execute(string)
                try:
                    cnx.commit()
                    return {"Success": True, "data": "Кошелек Успешно удален"}
                except:
                    return {"Success": False, "data": "Не удалось удалить кошелек"}
            if crud == 'status':
                string = "select * from pay_wallet_status "
                cur.execute(string)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}


async def crud_transfer(crud, payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                string_in = "SELECT id FROM user where " \
                            "email = '" + str(payload.user_id_in_email_or_login) \
                            + "' or login = '" + str(payload.user_id_in_email_or_login) + "' or id = '"\
                            + str(payload.user_id_in) + "'"
                cur.execute(string_in)
                data_in = cur.fetchone()
                user_in = data_in.get('id', 0)
                string_out = "SELECT id FROM user where " \
                             "email = '" + str(payload.user_id_out_email_or_login) \
                             + "' or login = '" + str(payload.user_id_out_email_or_login) + "' or id = '" \
                             + str(payload.user_id_in) + "'"
                cur.execute(string_out)
                data_out = cur.fetchone()
                user_out = data_out.get('id', 0)

                if user_out > 0 and user_in > 0:
                    string1 = "SELECT value FROM pay_balance where user_id = " + str(user_in)
                    cur.execute(string1)
                    data1 = cur.fetchone()
                    value_in = float(data1.get('value', 0))

                    string2 = "SELECT value FROM pay_balance where user_id = " + str(user_out)
                    cur.execute(string2)
                    data2 = cur.fetchone()
                    value_from = float(data2.get('value', 0))
                    if float(value_from) >= float(payload.value):
                        string3 = "UPDATE pay_balance SET value = " + str(value_in + payload.value) \
                                  + " where user_id = " + str(user_in)
                        cur.execute(string3)
                        cnx.commit()
                        string4 = "UPDATE pay_balance SET value = " + str(value_from - payload.value) \
                                  + " where user_id = " + str(user_out)
                        cur.execute(string4)
                        cnx.commit()
                        data_string = "INSERT INTO pay_transfer_history (user_id_in, user_id_out, value, status, date) " \
                                      "VALUES ('" + str(user_in) + "','" + str(user_out) + \
                                      "','" + str(payload.value) + "','1', NOW())"
                        cur.execute(data_string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            cnx.close()
                            return {"Success": True, "data": "Перевод успешно проведен"}
                        else:
                            cnx.close()
                            return {"Success": False, "data": "Не удалось совершить транзакцию перевода"}
                    else:
                        cnx.close()
                        return {"Success": False, "data": "Недостаточно баланса для совершения операции"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Выбранные пользователи не найдены"}

            if crud == 'get':
                if int(payload) == 0:
                    string1 = "SELECT user_id_in, user_id_out, value, status, DATE_FORMAT(date, "+str(config.date_format_all)+") as date " \
                              "FROM pay_transfer_history "
                else:
                    string1 = "SELECT user_id_in, user_id_out, value, status, DATE_FORMAT(date, "+str(config.date_format_all)+") as date " \
                              "FROM pay_transfer_history where " \
                              "user_id_in = '" + str(payload) + "' or " + "user_id_out = '" + str(payload) + "'"
                cur.execute(string1)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}
            if crud == "payin":
                frozen = payload.get('value')
                user_out = payload.get('user_id_out')
                user_in = payload.get('user_id_in')
                print("do emits", user_out, user_in, frozen)
                if user_in > 0 and user_out > 0:
                    print("emits", user_out, user_in, frozen)
                    string1 = "SELECT value FROM pay_balance where user_id = " + str(user_in)
                    cur.execute(string1)
                    data1 = cur.fetchone()
                    value_in = float(data1.get('value'))
                    string2 = "SELECT frozen FROM pay_balance where user_id = " + str(user_out)
                    cur.execute(string2)
                    data2 = cur.fetchone()
                    value_from = float(data2.get('frozen', 0))
                    if float(value_from) >= frozen:
                        # todo transaction multi
                        string3 = "UPDATE pay_balance SET value = " + str(value_in + frozen) \
                                  + " where user_id = " + str(user_in)
                        cur.execute(string3)
                        cnx.commit()
                        if cur.rowcount > 0:
                            string4 = "UPDATE pay_balance SET frozen = " + str(value_from - frozen) \
                                      + " where user_id = " + str(user_out)
                            cur.execute(string4)
                            cnx.commit()
                            if cur.rowcount > 0:
                                data_string = "INSERT INTO pay_transfer_history (user_id_in, user_id_out, value, status, date) " \
                                              "VALUES ('" + str(user_in) + "','" + str(user_out) + \
                                              "','" + str(payload.value) + "','1', NOW())"
                                cur.execute(data_string)
                                cnx.commit()
                                if cur.rowcount > 0:
                                    return {"Success": True, "data": "Перевод успешно проведен"}
                                else:
                                    return {"Success": False, "data": "Не удалось совершить транзакцию перевода"}
                            else:
                                return {"Success": False, "data": "Не удалось списать с баланса gjkexftnzk"}
                        else:
                            return {"Success": False, "data": "Не удалось списать с баланса отправителя"}
                    else:
                        return {"Success": False, "data": "Недостаточно баланса для совершения операции"}
                else:
                    return {"Success": False, "data": "Выбранные пользователи не найдены"}
