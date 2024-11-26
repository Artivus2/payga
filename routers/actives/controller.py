import mysql.connector as cpy
import config


async def crud_balance_percent(crud, payload): # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """

    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_str = "INSERT INTO pay_pay_percent (user_id, chart_id, value, " \
                           "baldep_status_id, baldep_types_id, date) " \
                           "VALUES ('" + str(payload['user_id']) + "','" + str(payload['chart_id']) + "','" \
                           + str(payload['value']) + "','" + str(payload['baldep_status_id']) +\
                           str(payload['baldep_types_id']) + "', NOW())"
                cur.execute(data_str)
                cnx.commit()
                return {"Success": True, "data": "Операция проведена"}
            if crud == 'get':
                if int(payload) == 0:  # todo left join
                    string = "select * from pay_pay_percent where pay_status_id = 1"
                else:
                    string = "select value, chart_id from pay_pay_percent " \
                             "where pay_status_id = 1 and user_id = " + str(payload)
                cur.execute(string)
                data = cur.fetchall()
                return {"Success": True, "data": data}
            if crud == 'set':
                string = "UPDATE pay_pay_percent set percent = " \
                         "where pay_status_id = 1 and user_id = " + str(payload['user_id'])
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно изменен"}
            if crud == 'remove':
                string = "UPDATE pay_pay_percent set pay_percent_status = 0 " \
                         "where user_id = " + str(payload['user_id'])
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно удален"}
            cnx.close()
    return {"Success": False, "data": "Операцию провести не удалось"}


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
                string = ("INSERT INTO balance "
                 "(user_id, value, mains_chart_id, balance_status_id, balance_types_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
                cur.execute(string, payload)
                cnx.commit()
                return {"Success": True, "data": "Операция проведена"}
            if crud == 'get':
                if int(payload) == 0: #todo left join
                    string = "select * from pay_balance"
                else:
                    string = "select value, chart_id from pay_balance " \
                         "where user_id = " + str(payload)
                cur.execute(string)
                data = cur.fetchall()
                return {"Success": True, "data": data}
            if crud == 'set':
                string = "UPDATE balance set value = '" +payload['value'] + \
                         "where balance_types_id = 1 and user_id = " + str(payload['user_id'])
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно изменен"}
            if crud == 'remove':
                string = "UPDATE balance set balance_types_id = 0 " \
                         "where user_id = " + str(payload['user_id'])
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно удален"}
            cnx.close()
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
                string = ("INSERT INTO deposit "
                 "(user_id, value, status_id, types) "
                 "VALUES (%s, %s, %s, %s)")
                cur.execute(string, payload)
                cnx.commit()
                return {"Success": True, "data": "Операция проведена"}
            if crud == 'get':
                if int(payload) == 0:  # todo left join
                    string = "select * from pay_deposit"
                else:
                    string = "select * from pay_deposit " \
                             "where user_id = " + str(payload)
                cur.execute(string)
                data = cur.fetchall()
                return {"Success": True, "data": data}
            if crud == 'set':
                string = "UPDATE deposit set value = '" +payload['value'] + \
                         "where status_id = 1 and user_id = " + str(payload['user_id'])
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно изменен"}
            if crud == 'remove':
                string = "UPDATE balance set status_id = 0 " \
                         "where user_id = " + str(payload['user_id'])
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно удален"}
            cnx.close()
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


async def get_wallet_status_by_id(id):
    """

    :param status_id:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                string = "select id, title from pay_wallet_status"
            else:
                string = "select id, title from pay_wallet_status " \
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
