import mysql.connector as cpy
import config


async def crud_balance_percent(crud, payload): # todo -> admin
    """
    :param crud:
    :param payload:
    :return:
    """

    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            if crud == 'create':
                string = ("INSERT INTO pay_pay_percent "
                 "(user_id, pay_id, value, date, pay_status_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
                data_str = "INSERT INTO pay_pay_percent (user_id, pay_id, value, date, pay_status_id) " \
                           "VALUES ('" + str(payload['user_id']) + \
                           "','" + str(payload['pay_id']) + "','"+str(payload['value'])+"',NOW(), 1)"
                cur.execute(data_str)
                cnx.commit()
                return {"Success": True, "data": "Операция проведена"}
            if crud == 'get':
                string = "select value from pay_pay_percent " \
                         "where pay_status_id = 1 and user_id = " + str(payload)
                cur.execute(string)
                cur.fetchone()
                data = cur.fetchone()[0]
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
        with cnx.cursor() as cur:
            if crud == 'create':
                string = ("INSERT INTO balance "
                 "(user_id, value, mains_chart_id, balance_status_id, balance_types_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
                cur.execute(string, payload)
                cnx.commit()
                return {"Success": True, "data": "Операция проведена"}
            if crud == 'get':
                string = "select value, mains_chart_id from balance " \
                         "where balance_types_id = 1 and user_id = " + str(payload['user_id'])
                cur.execute(string)
                cur.fetchone()
                data = cur.fetchone() # todo dict
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
        with cnx.cursor() as cur:
            if crud == 'create':
                string = ("INSERT INTO deposit "
                 "(user_id, value, status_id, types) "
                 "VALUES (%s, %s, %s, %s)")
                cur.execute(string, payload)
                cnx.commit()
                return {"Success": True, "data": "Операция проведена"}
            if crud == 'get':
                string = "select value from deposit " \
                         "where status_id = 1 and user_id = " + str(payload['user_id'])
                cur.execute(string)
                cur.fetchone()
                data = cur.fetchone() # todo dict
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