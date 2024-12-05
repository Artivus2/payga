import datetime

import mysql.connector as cpy
import config


async def crud_balance_percent(crud, payload): # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """
    print(payload)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_str = "INSERT INTO pay_pay_percent (user_id, pay_id, value, date, pay_status_id) " \
                           "VALUES ('" + str(payload.user_id) + "','" + str(payload.pay_id) + "','" \
                           + str(payload.value) + "', NOW() , '" + str(payload.pay_status_id) + "')"
                try:
                    cur.execute(data_str)
                    cnx.commit()
                    return {"Success": True, "data": "Операция проведена"}
                except:
                    return {"Success": False, "data": "Операцию провести не удалось"}

            if crud == 'get':
                if int(payload) == 0:  # todo left join
                    string = "select user_id, pay_id, pay_pay.title as pay_title, " \
                             "value, date, pay_status_id, pay_pay_status.title as pay_status_title " \
                             "from pay_pay_percent " \
                             "LEFT JOIN pay_pay ON pay_pay_percent.pay_id = pay_pay.id " \
                             "LEFT JOIN pay_pay_status ON pay_pay_percent.pay_status_id = pay_pay_status.id "
                else:
                    string = "select user_id, pay_id, pay_pay.title as pay_title, " \
                             "value, date, pay_status_id, pay_pay_status.title as pay_status_title " \
                             "from pay_pay_percent " \
                             "LEFT JOIN pay_pay ON pay_pay_percent.pay_id = pay_pay.id " \
                             "LEFT JOIN pay_pay_status ON pay_pay_percent.pay_status_id = pay_pay_status.id " \
                             "where pay_status_id = 1 and user_id = " + str(payload)
                cur.execute(string)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data}
                else:
                    return {"Success": False, "data": "Нет данных"}
            if crud == 'set':
                string = "UPDATE pay_pay_percent set percent = " \
                         "where pay_status_id = 1 and user_id = " + str(payload.user_id)

                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно изменен"}
                else:
                    return {"Success": False, "data": "Не удалось изменить"}
            if crud == 'remove':
                string = "UPDATE pay_pay_percent set pay_percent_status = 0 " \
                         "where user_id = " + str(payload['user_id'])
                try:
                    cur.execute(string)
                    cnx.commit()
                    return {"Success": True, "data": "Успешно удален"}
                except:
                    return {"Success": False, "data": "Не удалось удалить"}
            cnx.close()



async def crud_balance(crud, payload): # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """
    print(payload)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_string = "INSERT INTO pay_balance (user_id, value, chart_id, baldep_status_id, baldep_types_id) " \
                              "VALUES ('" + str(payload['user_id']) + "','" + str(payload['value']) + \
                              "','" + str(payload['chart_id']) + "','" + str(payload['baldep_status_id']) + "','" + \
                              str(payload['baldep_types_id']) + "')"
                try:
                    cur.execute(data_string)
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Баланс пользователя создан"}
                except:
                    return {"Success": False, "data": "Баланс не может быть создан"}
            if crud == 'get':
                if int(payload) == 0: #todo left join
                    string = "select * from pay_balance"
                else:
                    string = "select user_id, value, chart_id, baldep_status_id, baldep_types_id, " \
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
                string = "UPDATE pay_balance SET value = '" +str(payload.value) + \
                         "' where baldep_status_id = 1 and user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно изменен"}
                else:
                    return {"Success": False, "data": "Не удалось изменить баланс"}
            if crud == 'remove':
                string = "UPDATE pay_balance set baldep_types_id = 0, baldep_status_id = 0, value = 0 " \
                         "where user_id = " + str(payload.user_id)
                try:
                    cur.execute(string)
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Успешно удален"}
                except:
                    return {"Success": False, "data": "Ну удалось обнулить баланс"}
            if crud == 'status':
                string = "UPDATE pay_balance set baldep_status_id = '"+str(payload.baldep_status_id) \
                         + "' where user_id = " + str(payload.user_id)
                cur.execute(string)
                try:
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Статус изменен"}
                except:
                    return {"Success": False, "data": "Не удалось имзенить статус"}
            if crud == 'type':
                string = "UPDATE pay_balance set baldep_types_id = '"+str(payload.baldep_types_id)+"' " \
                         "where user_id = " + str(payload.user_id)
                cur.execute(string)
                try:
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": "Тип изменен"}
                except:
                    return {"Success": False, "data": "Не удалось имзенить тип"}


    return {"Success": False, "data": "Операцию провести не удалось"}


async def crud_deposit(crud, payload): # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """
    print(payload)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_string = "INSERT INTO pay_deposit (user_id, value, baldep_status_id, baldep_types_id, description) " \
                              "VALUES ('" + str(payload.user_id) + "','" + str(payload.value) + \
                              "','" + str(payload.baldep_types_id) + "','" + str(payload.baldep_status_id) + "','" + \
                              str(payload.description) + "')"
                try:
                    cur.execute(data_string)
                    cnx.commit()
                    return {"Success": True, "data": "Депозит пользователя создан"}
                except:
                    return {"Success": False, "data": "Депозит не может быть создан"}
            if crud == 'get':
                if int(payload) == 0:
                    string = "select * from pay_deposit"
                else:
                    string = "select user_id, value, baldep_status_id, baldep_types_id, " \
                             "pay_baldep_types.title as pay_baldep_types_title, " \
                             "pay_baldep_status.title as pay_baldep_status_title, description " \
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
                string = "UPDATE pay_deposit set value = '" +str(payload.value) + \
                         "' where baldep_types_id = 1 and user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно изменен"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Не удалось изменить баланс"}
            if crud == 'remove':
                string = "UPDATE pay_deposit set baldep_types_id = 0, baldep_status_id = 0, value = 0 " \
                         "where user_id = " + str(payload.user_id)
                cur.execute(string)
                try:
                    cnx.commit()
                    return {"Success": True, "data": "Успешно удален"}
                except:
                    return {"Success": False, "data": "Не удалось удалить"}
            if crud == 'status':
                string = "UPDATE pay_deposit set baldep_status_id = '"+str(payload.baldep_status_id) \
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
                string = "UPDATE pay_deposit set baldep_types_id = '"+str(payload.baldep_types_id)+"' " \
                         "where user_id = " + str(payload.user_id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Тип изменен"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Не удалось имзенить тип"}

    return {"Success": False, "data": "Операцию провести не удалось"}


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



async def crud_wallet(crud, payload): # todo -> admin
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
                string = "UPDATE pay_wallet set wallet_status_id = '" +str(payload.wallet_status_id) + \
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
