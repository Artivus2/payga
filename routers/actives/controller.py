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
                    data_str = "INSERT INTO pay_pay_percent (user_id, pay_id, value, DATE_FORMAT(date, " + str(
                        config.date_format_all) + ") as date, pay_status_id) " \
                                                  "VALUES ('" + str(payload.user_id) + "','" + str(
                        payload.pay_id) + "','" \
                               + str(payload.value) + "', NOW() , '" + str(payload.pay_status_id) + "')"
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
                if int(payload) == 0:  # todo left join
                    dop = ""
                else:
                    dop = "where user_id = " + str(payload)
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
    print(payload)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                # todo проверить есть уже баланс insert or update
                data_string = "INSERT INTO pay_balance (user_id, value, chart_id, baldep_status_id, " \
                              "baldep_types_id, frozen) " \
                              "VALUES ('" + str(payload.user_id) + "','" + str(payload.value) + \
                              "','" + str(payload.chart_id) + "','" + str(payload.baldep_status_id) + "','" + \
                              str(payload.baldep_types_id) + "','" + str(payload.frozen) + "')"
                try:
                    cur.execute(data_string)
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Баланс пользователя создан"}
                except:
                    return {"Success": False, "data": "Баланс не может быть создан"}
            if crud == 'get':
                if int(payload) == 0:  # todo left join
                    string = "select * from pay_balance"
                else:
                    string = "select user_id, value, chart_id, baldep_status_id, baldep_types_id, frozen, " \
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
                    get_balance_id = "SELECT * from pay_balance where user_id = " + str(payload.user_id)
                    cur.execute(get_balance_id)
                    data = cur.fetchone()
                    if data:
                        balance_history_status_id = 1  # todo откуда берутся статусы узнать
                        string_history = "INSERT INTO pay_balance_history (user_id, balance_id, chart_id, " \
                                         "date, value, frozen, balance_history_status_id, description) " \
                                         "VALUES ('" + str(payload.user_id) + "','" + str(data.get('id')) \
                                         + "','" + str(data.get('chart_id')) + "',UTC_TIMESTAMP(),'" + str(
                            data.get('value')) \
                                         + "','" + str(data.get('frozen')) + "','" \
                                         + str(balance_history_status_id) + "','" \
                                         + str(data.get('description')) + "')"
                        cur.execute(string_history)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True, "data": "Успешно изменен"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить баланс"}
                else:
                    return {"Success": False, "data": "Данные не изменены"}
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
            if crud == 'frozen':
                string0 = "SELECT value, frozen FROM pay_balance where user_id = " + str(payload.user_id)
                cur.execute(string0)
                data0 = cur.fetchone()
                current_value = float(data0.get('value', 0))
                current_frozen = float(data0.get('frozen', 0))
                if current_frozen == 0:
                    if current_value > payload.value:
                        string = "UPDATE pay_balance set value = '" + str(current_value - payload.value) + \
                                 "', frozen = '" + str(current_frozen + payload.value) + \
                                 "' where user_id = " + str(payload.user_id)
                        cur.execute(string)
                        cnx.commit()
                        if cur.rowcount > 0:
                            cnx.close()
                            return {"Success": True, "data": "Изменены доступные средства баланса"}
                        else:
                            return {"Success": False, "data": "Не удалось изменить доступные средства баланса"}
                    else:
                        return {"Success": False, "data": "Недостаточно средств на балансе"}
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


async def crud_deposit(crud, payload):  # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_string = "INSERT INTO pay_deposit (user_id, value, baldep_status_id, baldep_types_id, frozen, description) " \
                              "VALUES ('" + str(payload.user_id) + "','" + str(payload.value) + \
                              "','" + str(payload.baldep_types_id) + "','" + str(payload.baldep_status_id) + "','" + \
                              str(payload.frozen) + "','" + str(payload.min_deposit) + "','" + str(payload.description) + "')"
                try:
                    cur.execute(data_string)
                    cnx.commit()
                    return {"Success": True, "data": "Минимальный депозит пользователя создан"}
                except:
                    return {"Success": False, "data": "Депозит не может быть создан"}
            if crud == 'get':
                if int(payload) == 0:
                    string = "select * from pay_deposit"
                else:
                    string = "select user_id, value, baldep_status_id, baldep_types_id, " \
                             "pay_baldep_types.title as pay_baldep_types_title, " \
                             "pay_baldep_status.title as pay_baldep_status_title, frozen, min_deposit, description " \
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
            if crud == 'set-min':
                string = "UPDATE pay_deposit set min_deposit = '" + str(payload.min_deposit) + \
                         "' where user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Минимальный депозит изменен"}
                else:
                    cnx.close()
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


async def dep_withdrawal_check(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            date_check_from_balance = "SELECT date FROM pay_balance_history where " \
                                      "user_id = '" + str(payload.user_id) + "' and " \
                                      "date < DATE_ADD(UTC_TIMESTAMP(), INTERVAL -1 month)"
            print(date_check_from_balance)
            cur.execute(date_check_from_balance)
            data = cur.fetchall()
            if data:
                return {"Success": False, "data": "Вы не можете выводить с депозита не прошел срок 1 месяц"}
            else:
                result = await crud_deposit("frozen", payload)
                if result["Success"]:
                    #todo add to history deposit
                    insert_string = "INSERT into pay_deposit_history (user_id, date, " \
                                    "balordep, value, withdrawal_status_id) VALUES ('" + str(payload.user_id) \
                                    + "', UTC_TIMESTAMP(), 1, '" + str(payload.frozen) + "',0)"
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


async def bal_withdrawal_check(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT value, frozen FROM pay_balance where baldep_status_id = 1" \
                           " and baldep_types_id = 1 and " \
                           "value > 0 and user_id = " + str(payload.user_id)
            cur.execute(check_string)
            data = cur.fetchone()
            if data:
                #переводим с value на frozen
                result = await crud_balance("frozen", payload)
                if result["Success"]:
                    # todo add to history balance
                    insert_string = "INSERT into pay_deposit_history (user_id, date, " \
                                    "balordep, value, withdrawal_status_id) VALUES ('" + str(payload.user_id) + "', " \
                                    + "UTC_TIMESTAMP(), 2, '" + str(payload.value) + "',0)"
                    cur.execute(insert_string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        return {"Success": True, "data": result['data'] + ". Успешно."}
                    else:
                        return {"Success": False, "data": result['data'] + ". Не выполнено."}
                else:
                    return {"Success": False, "data": result['data'] + ". Не найдено."}

async def bal_refunds_check(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_deposit = "SELECT * from pay_deposit where baldep_status_id = 1" \
                            " and baldep_types_id = 1 and " \
                            "user_id = " + str(payload.user_id)
            cur.execute(check_deposit)
            data = cur.fetchone()
            if data:
                min_deposit = float(data.get('min_deposit'))
                value = payload.value #на сколько пополняем
                deposit_current_value = float(data.get('value'))
                deposit_frozen = float(data.get('frozen'))
                if deposit_frozen > 0:
                    return {"Success": False, "data": "Депозит заморожен на сумму: "+str(deposit_frozen)+". Дождитесь подтверждения всех заявок на ввод / вывод."}
                else:
                    check_balance = "SELECT * from pay_balance where baldep_status_id = 1" \
                                    " and baldep_types_id = 1 and " \
                                    "user_id = " + str(payload.user_id)
                    cur.execute(check_balance)
                    data_bal = cur.fetchone()
                    if not data_bal:
                        return {"Success": False, "data": "Параметры баланса не найдены. Обратитесь к администратору"}
                    else:
                        # добавляем баланс и депозит
                        balance_current_value = float(data_bal.get('value'))
                        print("balance_current_value", balance_current_value)
                        print("deposit_current_value", deposit_current_value)
                        print("min_deposit", min_deposit)
                        if deposit_current_value < min_deposit:
                            if value <= min_deposit - deposit_current_value:
                                payload.value = deposit_current_value + value
                                result_dep = await crud_deposit("set", payload)
                                if result_dep["Success"]:
                                    return {"Success": True, "data": "Депозит и баланс изменены"}
                            else:
                                payload.value = balance_current_value + value - min_deposit + deposit_current_value
                                result_bal = await crud_balance("set", payload)
                                if result_bal["Success"]:
                                    return {"Success": True, "data": "Баланс пополнен"}
                        else:
                            payload.value = balance_current_value + value
                            result_bal = await crud_balance("set", payload)
                            if result_bal["Success"]:
                                return {"Success": True, "data": "Баланс пополнен. Депозит в норме"}







                        # if value >= min_deposit - deposit_current_value:
                        #     insert_deposit = min_deposit
                        #     insert_balance = balance_current_value + value - (min_deposit - deposit_current_value)
                        #     payload.value = insert_deposit
                        #     if min_deposit != deposit_current_value:
                        #         result_dep = await crud_deposit("set", payload)
                        #         if result_dep["Success"]:
                        #             payload.value = insert_balance
                        #             result_bal = await crud_balance("set", payload)
                        #             if result_bal["Success"]:
                        #                 #insert_history_dep
                        #                 return {"Success": True,
                        #                         "data": "Депозит дополнен, остатки поступили на баланс"}
                        #             else:
                        #                 return {"Success": False,
                        #                         "data": "Депозит и баланс не пополнены. Обратитесь к администратору"}
                        # else:
                        #     insert_deposit = deposit_current_value + value
                        #     payload.value = insert_deposit
                        #     result_dep = await crud_deposit("set", payload)
                        #     if result_dep["Success"]:
                        #         return {"Success": True,
                        #                 "data": "Депозит дополнен, остатки поступили на баланс"}
                        #     else:
                        #         return {"Success": False,
                        #                 "data": "Депозит не пополнен. Обратитесь к администратору"}












            else:
                return {"Success": False, "data": "Баланс не активирован. Обратитесь к администратору"}


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
                            + "' or login = '" + str(payload.user_id_in_email_or_login) + "'"
                cur.execute(string_in)
                data_in = cur.fetchone()
                user_in = data_in.get('id', 0)
                string_out = "SELECT id FROM user where " \
                             "email = '" + str(payload.user_id_out_email_or_login) \
                             + "' or login = '" + str(payload.user_id_out_email_or_login) + "'"
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
