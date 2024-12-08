import mysql.connector as cpy
import config
from routers.orders.utils import generate_uuid


async def get_bank(id):
    """
    Найти банк по id, 0 - все банки
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                data = "SELECT id, title from banks where title not like ''"
            else:
                data = "SELECT id, title from banks where title not like '' and id = " + str(id)
            cur.execute(data)
            data = cur.fetchall()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                cnx.close()
                return {"Success": False, "data": 'банк не найден'}


async def get_chart(id):
    """
    Найти крипту по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                data = "SELECT id, symbol from chart"
            else:
                data = "SELECT id, symbol from chart where id = " + str(id)
            cur.execute(data)
            data = cur.fetchall()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'Валюта не найдена'}


async def get_curr(id):
    """
    Найти валюту по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                data = "SELECT id, symbol from currency"
            else:
                data = "SELECT id, symbol from currency where id = " + str(id)
            cur.execute(data)
            data = cur.fetchall()
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
            string = "SELECT user_id, pay_reqs.id, pay_reqs.uuid, pay_reqs.title " \
                   "req_group_id, pay_reqs_groups.title as pay_reqs_groups_title," \
                   "sequence, pay_pay_id, pay_pay.title as pay_title," \
                   "pay_reqs_status.title as pay_status,  pay_reqs.value," \
                   "reqs_types_id, pay_reqs_types.title as reqs_types_title," \
                   "bank_id, banks.title as bank_title, currency_id, currency.symbol as currency_symbol," \
                   "phone, pay_reqs.date, " \
                   "qty_limit_hour, qty_limit_day, qty_limit_month, sum_limit_hour, sum_limit_day, " \
                   "sum_limit_month, limit_active_orders, other_banks, min_sum_per_transaction, " \
                   "max_sum_per_transaction, max_limit_transaction_sum, max_limit_transaction" \
                   "from pay_reqs " \
                   "LEFT JOIN banks ON pay_reqs.bank_id = banks.id " \
                   "LEFT JOIN currency ON pay_reqs.currency_id = currency.id " \
                   "LEFT JOIN pay_reqs_groups ON pay_reqs.req_group_id = pay_reqs_groups.id " \
                   "LEFT JOIN pay_reqs_status ON pay_reqs.reqs_status_id = pay_reqs_status.id " \
                   "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                   "LEFT JOIN pay_pay ON pay_reqs.pay_pay_id = pay_pay.id " \
                   "where user_id = " + str(user_id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'Реквизиты не найдены'}


async def set_reqs_by_any(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_update = "UPDATE pay_reqs SET "
            for k, v in dict(payload).items():
                if k != 'user_id':
                    data_update += str(k) + " = '" + str(v) + "',"
            data_update = data_update[:-1]
            data_update += " where user_id = " + str(payload.get('user_id'))
            cur.execute(data_update)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Реквизиты успешно обновлены"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты не обновлены"}


async def remove_reqs_by_id(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "DELETE FROM pay_reqs where id = " + str(id)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Реквизиты успешно удалены"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты не удалены"}

async def get_reqs_groups_by_id(id):
    """
    Найти реквизиты группы по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            print(id)

            if int(id) == 0:
                data = "SELECT pay_reqs_groups.title, pay_reqs_groups.id, pay_reqs_groups.uuid as group_uuid," \
                       "pay_reqs.id, pay_reqs.uuid as reqs_uuid, pay_reqs.date," \
                       "types_automate_id, pay_automation_type.title as types_automation_title," \
                       "pay_automation_turn_off.id as turn_off_id, pay_automation_turn_off.title as turn_off_status " \
                       "from pay_reqs_groups " \
                       "LEFT JOIN pay_reqs ON pay_reqs_groups.id = pay_reqs.req_group_id " \
                       "LEFT JOIN pay_automation_type ON pay_reqs_groups.types_automate_id = pay_automation_type.id " \
                       "LEFT JOIN pay_automation_turn_off ON pay_reqs_groups.turn_off = pay_automation_turn_off.id"
            else:
                data = "SELECT pay_reqs_groups.title, pay_reqs_groups.id, pay_reqs_groups.uuid as group_uuid," \
                       "pay_reqs.id, pay_reqs.uuid as reqs_uuid, pay_reqs.date," \
                       "types_automate_id, pay_automation_type.title as types_automation_title," \
                       "pay_automation_turn_off.id as turn_off_id, pay_automation_turn_off.title as turn_off_status " \
                       "from pay_reqs_groups " \
                       "LEFT JOIN pay_reqs ON pay_reqs_groups.id = pay_reqs.req_group_id " \
                       "LEFT JOIN pay_automation_type ON pay_reqs_groups.types_automate_id = pay_automation_type.id " \
                       "LEFT JOIN pay_automation_turn_off ON pay_reqs_groups.turn_off = pay_automation_turn_off.id " \
                       "where pay_reqs.id = " + str(id)

            cur.execute(data)
            data = cur.fetchall()
            if data:
                cnx.close()
                return {"Success": True, "data": data}
            else:
                cnx.close()
                return {"Success": False, "data": 'группа не найдена'}


async def set_reqs_group_by_any(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_update = "UPDATE pay_reqs_groups SET "
            for k, v in dict(payload).items():
                if k != 'id':
                    data_update += str(k) + " = '" + str(v) + "',"
            data_update = data_update[:-1]
            data_update += " where id = " + str(payload.get('id'))
            cur.execute(data_update)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно обновлены реквизиты группы"}
            else:
                cnx.close()
                return {"Success": False, "data": "реквизиты группы не обновлены"}


async def req_by_filters(payload):
    """
    Найти реквизиты по фильтрам
    :param payload:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            #null_id = payload.get('id', 0)
            data = "SELECT pay_reqs.id, pay_reqs.uuid, pay_reqs.title," \
                   "req_group_id, pay_reqs_groups.title as pay_reqs_groups_title," \
                   "sequence, pay_pay_id, pay_pay.title as pay_title," \
                   "pay_reqs_status.title as pay_status,  pay_reqs.value," \
                   "reqs_types_id, pay_reqs_types.title as reqs_types_title," \
                   "bank_id, banks.title as bank_title, currency_id, currency.symbol as currency_symbol," \
                   "phone, pay_reqs.date, qty_limit_hour, qty_limit_day, qty_limit_month, " \
                   "sum_limit_hour, sum_limit_day, sum_limit_month, limit_active_orders, other_banks, " \
                   "min_sum_per_transaction, max_sum_per_transaction, max_limit_transaction_sum," \
                   "max_limit_transaction " \
                   "from pay_reqs " \
                   "LEFT JOIN banks ON pay_reqs.bank_id = banks.id " \
                   "LEFT JOIN currency ON pay_reqs.currency_id = currency.id " \
                   "LEFT JOIN pay_reqs_groups ON pay_reqs.req_group_id = pay_reqs_groups.id " \
                   "LEFT JOIN pay_reqs_status ON pay_reqs.reqs_status_id = pay_reqs_status.id " \
                   "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                   "LEFT JOIN pay_pay ON pay_reqs.pay_pay_id = pay_pay.id " \
                   "where "
            # if int(null_id) == 0:
            #     data += "pay_reqs.id > 0"
            # else:
            for k, v in dict(payload).items():
                data += "pay_reqs." + str(k) + " = '" + str(v) + "' and "
            data += "pay_reqs.id is not null"

            cur.execute(data)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Реквизиты не найдены"}


async def get_automation_status(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_automation_status"
            else:
                string = "SELECT * FROM pay_automation_status where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Автоматизации не найдены"}


async def get_automation_type(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_automation_type"
            else:
                string = "SELECT * FROM pay_automation_type where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Типы автоматизации не найдены"}


async def get_pay_reqs_status_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_reqs_status"
            else:
                string = "SELECT * FROM pay_reqs_status where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Статусы не найдены"}


async def get_pay_reqs_types_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_reqs_types"
            else:
                string = "SELECT * FROM pay_reqs_types where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Статусы не найдены"}


async def get_turn_off(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_automation_turn_off"
            else:
                string = "SELECT * FROM pay_automation_turn_off where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Статусы ыключения не найдены"}


async def create_reqs_for_user(payload):
    """
    axios.post('/api/v1/mains/create-reqs',{
      title: 'sgsg',
      user_id: 638,
      req_group_id: 0,
      sequence: 100,
      pay_pay_id: 1,
      value: 'sdfsdfsdf',
      currency_id: 1,
      reqs_types_id: 1,
      reqs_status_id: 1,
      bank_id: 142,
      chart_id: 259,
      phone: '+545674567',
      qty_limit_hour: 1,
      qty_limit_day: 10,
      qty_limit_month: 100,
      sum_limit_hour: 300,
      sum_limit_day: 10000,
      sum_limit_month: 100000,
      limit_active_orders: 1,
      other_banks: 1,
      min_sum_per_transaction:1,
      max_sum_per_transaction:1,
      max_limit_transaction_sum:1,
      max_limit_transaction: 1

  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            uuids = await generate_uuid()
            print(payload)
            data_string = "INSERT INTO pay_reqs (uuid, user_id, req_group_id, sequence, pay_pay_id, value," \
                          "currency_id, reqs_types_id, reqs_status_id, bank_id, phone, date, qty_limit_hour," \
                          "qty_limit_day, qty_limit_month, sum_limit_hour, sum_limit_day, sum_limit_month," \
                          "title, limit_active_orders, other_banks, min_sum_per_transaction," \
                          "max_sum_per_transaction, max_limit_transaction_sum, max_limit_transaction) " \
                          "VALUES ('" + str(uuids) + "','" + str(payload.user_id) + \
                          "',0,'" + str(payload.sequence) + "','" + \
                          str(payload.pay_pay_id) + "','" + str(payload.value) + "','" \
                          + str(payload.currency_id) + "','" + str(payload.reqs_types_id) + "','" \
                          + str(payload.reqs_status_id) + "','" + str(payload.bank_id) + "','" \
                          + str(payload.phone) + "',NOW(),'" + str(payload.qty_limit_hour) \
                          + "','" + str(payload.qty_limit_day) + "','" + str(payload.qty_limit_month) \
                          + "','" + str(payload.sum_limit_hour) + "','" + str(payload.sum_limit_day) \
                          + "','" + str(payload.sum_limit_month) + "','" + str(payload.title) \
                          + "','" + str(payload.limit_active_orders) + "','" + str(payload.other_banks) \
                          + "','" + str(payload.min_sum_per_transaction) + "','" + str(payload.max_sum_per_transaction) \
                          + "','" + str(payload.max_limit_transaction_sum) + "','" + str(payload.max_limit_transaction) \
                          + "')"
            cur.execute(data_string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно добавлены реквизиты"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты не добавлены"}


async def create_reqs_group(payload):
    """
    title: str | None = None
    types_automate_id: int | None = None
    turn_off: int | None = None
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            uuids = await generate_uuid()
            print(payload)
            string = "INSERT INTO pay_reqs_groups (uuid, reqs_id, date, title, types_automate_id, turn_off) " \
                     "VALUES('"+str(uuids)+"',0, NOW(),'"+str(payload.title)+"',"+str(payload.types_automate_id)\
                     +",'"+str(payload.turn_off)+"')"
            print(string)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно добавлены реквизиты группы"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты группы не добавлены"}


async def add_reqs_by_id_to_group(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            print(payload.id_group)
            string = "UPDATE pay_reqs SET req_group_id = '" + str(payload.id_group)\
                     + "' where id = " + str(payload.id_reqs)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно добавлен в группу"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты в группу не добавлены"}



async def remove_reqs_by_id_from_group(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_reqs SET req_group_id = 0 where id = " + str(payload.id_reqs)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно удален из группы"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты из группы не удалены"}


async def get_automation_history(payload):
    pass