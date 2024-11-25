import mysql.connector as cpy
import config


async def get_bank(id):
    """
    Найти банк по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data = "SELECT id, bank from bank where id = " + str(id)
            cur.execute(data)
            data = cur.fetchone()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'банк не найден'}


async def get_chart(id):
    """
    Найти крипту по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data = "SELECT id, symbol from chart where id = " + str(id)
            cur.execute(data)
            data = cur.fetchone()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'Валюта не найдена'}


async def get_reqs_by_user(user_id):
    """
    Найти реквизиты по user_id
    :param user_id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data = "SELECT pay_reqs.id, pay_reqs.uuid," \
                   "req_group_id, pay_reqs_groups.title as pay_reqs_groups_title," \
                   "sequence, pay_pay_id, pay_pay.title as pay_title," \
                   "pay_reqs_status.title as pay_status,  pay_reqs.value," \
                   "reqs_types_id, pay_reqs_types.title as reqs_types_title," \
                   "bank_id, banks.title as bank_title, currency_id, currency.symbol as currency_symbol," \
                   "phone, pay_reqs.date, " \
                   "qty_limit_hour, qty_limit_day, qty_limit_month, sum_limit_hour, sum_limit_day, sum_limit_month " \
                   "from pay_reqs " \
                   "LEFT JOIN banks ON pay_reqs.bank_id = banks.id " \
                   "LEFT JOIN currency ON pay_reqs.currency_id = currency.id " \
                   "LEFT JOIN pay_reqs_groups ON pay_reqs.req_group_id = pay_reqs_groups.id " \
                   "LEFT JOIN pay_reqs_status ON pay_reqs.reqs_status_id = pay_reqs_status.id " \
                   "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                   "LEFT JOIN pay_pay ON pay_reqs.pay_pay_id = pay_pay.id " \
                   "where user_id = " + str(user_id)
            cur.execute(data)
            data = cur.fetchone()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'Валюта не найдена'}


async def get_reqs_groups_by_id(id):
    """
    Найти реквизиты группы по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data = "SELECT pay_reqs_groups.id, pay_reqs_groups.uuid as group_uuid," \
                   "pay_reqs.id, pay_reqs.uuid as reqs_uuid, pay_reqs.date," \
                   "types_automate_id, pay_automation_type.title as types_automation_title," \
                   "pay_automation_turn_off.id as turn_off_id, pay_automation_turn_off.title as turn_off_status " \
                   "from pay_reqs_groups " \
                   "LEFT JOIN pay_reqs ON pay_reqs_groups.id = pay_reqs.req_group_id " \
                   "LEFT JOIN pay_automation_type ON pay_reqs_groups.types_automate_id = pay_automation_type.id " \
                   "LEFT JOIN pay_automation_turn_off ON pay_reqs_groups.turn_off = pay_automation_turn_off.id " \
                   "where pay_reqs.id = " + str(id)

            cur.execute(data)
            data = cur.fetchone()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'группа не найдена'}


async def req_by_filters(payload):
    """
    Найти реквизиты группы по id
    :param payload:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            null_id = payload.get('id', 0)
            data = "SELECT pay_reqs.id, pay_reqs.uuid," \
                   "req_group_id, pay_reqs_groups.title as pay_reqs_groups_title," \
                   "sequence, pay_pay_id, pay_pay.title as pay_title," \
                   "pay_reqs_status.title as pay_status,  pay_reqs.value," \
                   "reqs_types_id, pay_reqs_types.title as reqs_types_title," \
                   "bank_id, banks.title as bank_title, currency_id, currency.symbol as currency_symbol," \
                   "phone, pay_reqs.date, " \
                   "qty_limit_hour, qty_limit_day, qty_limit_month, sum_limit_hour, sum_limit_day, sum_limit_month " \
                   "from pay_reqs " \
                   "LEFT JOIN banks ON pay_reqs.bank_id = banks.id " \
                   "LEFT JOIN currency ON pay_reqs.currency_id = currency.id " \
                   "LEFT JOIN pay_reqs_groups ON pay_reqs.req_group_id = pay_reqs_groups.id " \
                   "LEFT JOIN pay_reqs_status ON pay_reqs.reqs_status_id = pay_reqs_status.id " \
                   "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                   "LEFT JOIN pay_pay ON pay_reqs.pay_pay_id = pay_pay.id " \
                   "where "
            if int(null_id) == 0:
                data += "pay_reqs.id > 0"
            else:
                for k, v in dict(payload).items():
                    data += "pay_reqs." + str(k) + " = '" + str(v) + "' and "
                data += "pay_reqs.id is not null"

            print(data)
            cur.execute(data)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Реквизиты не найдены"}
