import mysql.connector as cpy
import config
from routers.admin.utils import send_mail
from routers.orders.utils import generate_uuid


async def get_banks(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if id == 0:
                select_banks = "SELECT * FROM pay_admin_banks"
            else:
                select_banks = "SELECT * FROM pay_admin_banks where active = 1"
            cur.execute(select_banks)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'банки не найдены'}



async def get_fav_bank(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:

            data_string = "SELECT pay_fav_banks.id, pay_admin_banks.title, pay_admin_banks.bik, pay_fav_banks.active " \
                   "from pay_fav_banks " \
                   "LEFT JOIN pay_admin_banks ON pay_fav_banks.bank_id = pay_admin_banks.id  " \
                   "where pay_admin_banks.active = 1 and user_id = " + str(user_id)
            cur.execute(data_string)

            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'банк не найден'}

async def set_admin_bank(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT * from pay_admin_banks where " \
                           "id = " + str(payload.get('id',0))
            cur.execute(check_string)
            adm_banks = cur.fetchall()
            if adm_banks:
                data_update = "UPDATE pay_admin_banks SET "
                for k, v in dict(payload).items():
                    print(k,v)
                    if k != 'id':
                        data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where id = " + str(payload.get('id'))
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Банк изменен"}
                else:
                    return {"Success": False, "data": "банк не изменен"}

            else:
                insert_string = "INSERT INTO pay_admin_banks (title, bik, active) " \
                                "VALUES ('" + str(payload.get('title')) + \
                                "','" + str(payload.get('bik')) + "', 1)"
                cur.execute(insert_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Банк успешно добавлен"}
                else:
                    return {"Success": False, "data": "банк не добавлен"}


async def set_fav_bank(payload): #todo fav_banks
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT * from pay_fav_banks where " \
                           "user_id = " + str(payload.user_id) + " and bank_id = '" + str(payload.bank_id) + "'"
            cur.execute(check_string)
            fav_banks = cur.fetchall()
            if fav_banks:
                update_string = "UPDATE pay_fav_banks set " \
                                "active = '" + str(payload.active) + "' where user_id = " + str(payload.user_id)\
                                + " and bank_id = " + str(payload.bank_id)
                cur.execute(update_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Статус активности изменен"}
                else:
                    return {"Success": False, "data": "банк не изменен"}
            else:
                insert_string = "INSERT INTO pay_fav_banks (user_id, bank_id, active) " \
                                "VALUES (" + str(payload.user_id) +\
                                ",'" + str(payload.bank_id) + "', 1)"
                cur.execute(insert_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Успешно добавлен в группу избранных банков"}
                else:
                    return {"Success": False, "data": "банк в группу не добавлен"}


async def remove_admin_bank(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            delete_string = "DELETE FROM pay_admin_banks where " \
                            "id = '" + str(payload.id) + "'"
            cur.execute(delete_string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно удален из admin банков"}
            else:
                cnx.close()
                return {"Success": False, "data": "банк не найден"}


async def remove_fav_bank(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            delete_string = "DELETE FROM pay_fav_banks where " \
                            "id = '"+str(payload.id) + "'"
            cur.execute(delete_string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно удален из группы избранных банков"}
            else:
                cnx.close()
                return {"Success": False, "data": "банк не найден"}


async def get_chart(id=0):
    """
    Найти крипту по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(id) == 0:
                data = "SELECT id, symbol from chart where active = 1"
            else:
                data = "SELECT id, symbol from chart where active = 1 and id = " + str(id)
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


async def set_reqs_by_any(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_orders = "SELECT * FROM pay_orders where req_id = " + str(payload.get('id'))
            cur.execute(string_orders)
            orders = cur.fetchall()
            if not orders:
                data_update = "UPDATE pay_reqs SET "
                for k, v in dict(payload).items():
                    if k != 'id':
                        data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where id = " + str(payload.get('id'))
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Реквизиты успешно обновлены"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Реквизиты не обновлены"}
            else:
                return {"Success": False, "data": "Редактирование платежной информации невозможно, c реквизитами уже были созданы ордера"}


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


async def remove_group_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "UPDATE pay_reqs SET req_group_id = 0 WHERE user_id = '" +str(payload.user_id) \
                      + "' and req_group_id = '" + str(payload.id) + "'"
            cur.execute(string0)
            cnx.commit()
            string1 = "DELETE FROM pay_reqs_groups WHERE id = " + str(payload.id)\
                  + " and user_id = " + str(payload.user_id)
            cur.execute(string1)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Группа реквизитов успешно удалена"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты группы не удалены"}




async def get_reqs_groups_by_id(user_id):
    """
    Найти реквизиты группы по id
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            print(id)

            if int(user_id) == 0:
                data = "SELECT pay_reqs_groups.title, pay_reqs_groups.id, pay_reqs_groups.uuid as group_uuid," \
                       "pay_reqs_groups.user_id, " \
                       "types_automate_id, pay_automation_type.title as types_automation_title," \
                       "pay_automation_turn_off.id as turn_off_id, pay_automation_turn_off.title as turn_off_status," \
                       "pay_api_keys.api_key, pay_api_keys.api_key_expired_date " \
                       "from pay_reqs_groups " \
                       "LEFT JOIN pay_automation_type ON pay_reqs_groups.types_automate_id = pay_automation_type.id " \
                       "LEFT JOIN pay_automation_turn_off ON pay_reqs_groups.turn_off = pay_automation_turn_off.id " \
                       "LEFT JOIN pay_api_keys ON pay_reqs_groups.user_id = pay_api_keys.user_id"
            else:
                data = "SELECT pay_reqs_groups.title, pay_reqs_groups.id, pay_reqs_groups.uuid as group_uuid," \
                       "pay_reqs_groups.user_id, " \
                       "types_automate_id, pay_automation_type.title as types_automation_title," \
                       "pay_automation_turn_off.id as turn_off_id, pay_automation_turn_off.title as turn_off_status," \
                       "pay_api_keys.api_key, pay_api_keys.api_key_expired_date " \
                       "from pay_reqs_groups " \
                       "LEFT JOIN pay_automation_type ON pay_reqs_groups.types_automate_id = pay_automation_type.id " \
                       "LEFT JOIN pay_automation_turn_off ON pay_reqs_groups.turn_off = pay_automation_turn_off.id " \
                       "LEFT JOIN pay_api_keys ON pay_reqs_groups.user_id = pay_api_keys.user_id " \
                       "where pay_reqs_groups.user_id = " + str(user_id)

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
                return {"Success": True, "data": "Успешно обновлены реквизиты группы"}
            else:
                return {"Success": False, "data": "реквизиты группы не обновлены"}


async def get_payout_reqs(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string ="SELECT * FROM pay_orders_payout_reqs where order_id = " + str(payload)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "реквизиты не найдены"}


async def req_by_filters(payload):
    """
    Найти реквизиты по фильтрам
    :param payload:
    :param id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # null_id = payload.get('id', 0)
            string = "SELECT pay_reqs.user_id, pay_reqs.id, pay_reqs.uuid as pay_reqs_uuid, pay_reqs.title, " \
                     "req_group_id, pay_reqs_groups.title as pay_reqs_groups_title," \
                     "pay_reqs_groups.types_automate_id as pay_automation_type_id, pay_reqs_groups.turn_off, " \
                     "pay_reqs_groups.uuid as pay_reqs_groups_uuid, " \
                     "sequence, pay_pay_id, pay_pay.title as pay_title," \
                     "pay_reqs_status.title as pay_status, pay_reqs.value, pay_reqs.short_value," \
                     "reqs_types_id, pay_reqs_types.title as reqs_types_title," \
                     "pay_admin_banks.id as bank_id, pay_admin_banks.title as bank_title, currency_id, currency.symbol as currency_symbol," \
                     "fio, DATE_FORMAT(pay_reqs.date, "+str(config.date_format_all)+") as date, pay_automation_type.title as pay_automation_type_title, " \
                     "pay_automation_turn_off.title as turn_off_title," \
                     "qty_limit_hour, qty_limit_day, qty_limit_month, sum_limit_hour, sum_limit_day, " \
                     "sum_limit_month, limit_active_orders, other_banks, min_sum_per_transaction, " \
                     "max_sum_per_transaction, max_limit_transaction_sum, max_limit_transaction " \
                     "from pay_reqs " \
                     "LEFT JOIN pay_admin_banks ON pay_admin_banks.id = pay_reqs.bank_id " \
                     "LEFT JOIN currency ON pay_reqs.currency_id = currency.id " \
                     "LEFT JOIN pay_reqs_groups ON pay_reqs.req_group_id = pay_reqs_groups.id " \
                     "LEFT JOIN pay_reqs_status ON pay_reqs.reqs_status_id = pay_reqs_status.id " \
                     "LEFT JOIN pay_reqs_types ON pay_reqs.reqs_types_id = pay_reqs_types.id " \
                     "LEFT JOIN pay_pay ON pay_reqs.pay_pay_id = pay_pay.id " \
                     "LEFT JOIN pay_automation_type ON pay_reqs_groups.types_automate_id = pay_automation_type.id " \
                     "LEFT JOIN pay_automation_turn_off ON pay_reqs_groups.id = pay_automation_turn_off.id " \
                     "where "
            # if int(null_id) == 0:
            #     data += "pay_reqs.id > 0"
            # else:
            for k, v in dict(payload).items():
                if k != 'date_start' and k != 'date_end':
                    string += "pay_reqs." + str(k) + " = '" + str(v) + "' and "

            string += "pay_reqs.id is not null"
            try: #todo эталон фильтр по датам
                if payload['date_start'] is not None and payload['date_end'] is not None:
                    string += " and pay_reqs.date >= '" + str(payload['date_start']) \
                              + " 00:00' and pay_reqs.date <= '" + str(payload['date_end']) + " 23:59'"
            except:
                print("фильтр по датам не выбран")
            print(string)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
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


async def set_pay_reqs_types_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM pay_reqs_types where id = " + str(payload.id)
            cur.execute(string0)
            data0 = cur.fetchall()
            if data0:
                string = "UPDATE pay_reqs_types SET title = '" + str(payload.title) \
                         + "' where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно обновлен платежный метод"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Платежный метод не обновлен"}
            else:
                string = "INSERT INTO pay_reqs_types (title) " \
                         "VALUES('" + str(payload.title) + "')"
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно добавлен платежный метод"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Платежный метод не добавлены"}



async def remove_pay_reqs_types_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "DELETE FROM pay_reqs_types where id = " + str(payload.id)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Платежный метод удален"}
            else:
                cnx.close()
                return {"Success": False, "data": "Платежный метод не может быть удален"}


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
      reqs_status_id: 0,
      bank_id: 142,
      chart_id: 259,
      fio: 'fio',
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
            if payload.req_group_id is None:
                payload.req_group_id = 0
            data_string = "INSERT INTO pay_reqs (uuid, user_id, req_group_id, sequence, pay_pay_id, value," \
                          "currency_id, reqs_types_id, reqs_status_id, bank_id, fio, date, qty_limit_hour," \
                          "qty_limit_day, qty_limit_month, sum_limit_hour, sum_limit_day, sum_limit_month," \
                          "title, limit_active_orders, other_banks, min_sum_per_transaction," \
                          "max_sum_per_transaction, max_limit_transaction_sum, max_limit_transaction) " \
                          "VALUES ('" + str(uuids) + "','" + str(payload.user_id) + \
                          "','"+str(payload.req_group_id)+"','" + str(payload.sequence) + "','" + \
                          str(payload.pay_pay_id) + "','" + str(payload.value) + "','" \
                          + str(payload.currency_id) + "','" + str(payload.reqs_types_id) + "',0,'" \
                          + str(payload.bank_id) + "','" \
                          + str(payload.fio) + "',NOW(),'" + str(payload.qty_limit_hour) \
                          + "','" + str(payload.qty_limit_day) + "','" + str(payload.qty_limit_month) \
                          + "','" + str(payload.sum_limit_hour) + "','" + str(payload.sum_limit_day) \
                          + "','" + str(payload.sum_limit_month) + "','" + str(payload.title) \
                          + "','" + str(payload.limit_active_orders) + "','" + str(payload.other_banks) \
                          + "','" + str(payload.min_sum_per_transaction) + "','" \
                          + str(payload.max_sum_per_transaction) \
                          + "','" + str(payload.max_limit_transaction_sum) + "','" \
                          + str(payload.max_limit_transaction) \
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
    user_id: int
    turn_off: int | None = None
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            uuids = await generate_uuid()
            print(payload)
            string = "INSERT INTO pay_reqs_groups (uuid, date, title, types_automate_id, turn_off, user_id) " \
                     "VALUES('" + str(uuids) + "', NOW(),'" + str(payload.title) + "'," + str(
                payload.types_automate_id) + ",'" + str(payload.turn_off) + "', '"+str(payload.user_id)+"')"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                string_check = "SELECT id from pay_reqs_groups where uuid = '" + str(uuids) + "'"
                cur.execute(string_check)
                data = cur.fetchone()
                cnx.close()
                return {"Success": True, "data": data['id']}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты группы не добавлены"}


async def add_reqs_by_id_to_group(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if isinstance(payload.id_reqs, list):
                for i in list(payload.id_reqs):
                    check_blocked_or_inactive = "SELECT * from pay_reqs where reqs_status_id = 1 and id = " + str(i)
                    cur.execute(check_blocked_or_inactive)
                    data0 = cur.fetchone()
                    if data0:
                        string = "UPDATE pay_reqs SET req_group_id = '" + str(payload.id_group) \
                                 + "' where id = " + str(i)
                        cur.execute(string)
                        cnx.commit()
            else:
                check_blocked_or_inactive = "SELECT * from pay_reqs where " \
                                            "reqs_status_id = 1 and id = " + str(payload.id_reqs)
                cur.execute(check_blocked_or_inactive)
                data0 = cur.fetchone()
                if data0:
                    string = "UPDATE pay_reqs SET req_group_id = '" + str(payload.id_group) \
                             + "' where id = " + str(payload.id_reqs)
                    cur.execute(string)
                    cnx.commit()
            if cur.rowcount > 0:
                return {"Success": True, "data": "Успешно добавлен в группу"}
            else:
                return {"Success": False, "data": "Реквизиты в группу не добавлены. "
                                                  "Реквизиты не активны или заблокированы"}


async def remove_reqs_by_id_from_group(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if isinstance(payload.id_reqs, list):
                for i in list(payload.id_reqs):
                    string = "UPDATE pay_reqs SET req_group_id = 0 where id = " + str(i)
                    cur.execute(string)
                    cnx.commit()
            else:
                string = "UPDATE pay_reqs SET req_group_id = 0 where id = " + str(payload.id_reqs)
                cur.execute(string)
                cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно добавлен в группу"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реквизиты в группу не добавлены"}


async def get_automation_history(payload):
    pass


async def get_pay_refs_types_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_refs_types"
            else:
                string = "SELECT * FROM pay_refs_types where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Типы рефералов не найдены"}


async def set_or_create_pay_refs_types_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM pay_refs_types where id = " + str(payload.id)
            cur.execute(string0)
            data0 = cur.fetchall()
            if data0:
                string = "UPDATE pay_refs_types SET title = '" + str(payload.title) \
                         + "' where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно обновлен тип реферала"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Типы рефералов не обновлены"}
            else:
                string = "INSERT INTO pay_refs_types (title) " \
                         "VALUES('" + str(payload.title) + "')"
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Успешно добавлен тип реферала"}
                else:
                    cnx.close()
                    return {"Success": False, "data": "Типы рефералов не добавлены"}


async def get_pay_refs_levels_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_refs_levels"
            else:
                string = "SELECT * FROM pay_refs_levels where id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Уровни рефералов не найдены"}


async def update_pay_refs_level_by_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_refs_level SET title = " + str(payload.title) \
                     + ", value = '" + str(payload.value) + "' where id = " + str(payload.id)
            cur.execute(string)
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно обновлен уровень реферальной программы"}
            else:
                cnx.close()
                return {"Success": False, "data": "Реферальная программа не обновлена"}


async def get_pay_refs_by_user(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if int(payload) == 0:
                string = "SELECT * FROM pay_refs"
            else:
                string = "SELECT * FROM pay_refs where user_id = " + str(payload)
            cur.execute(string)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Рефералы не найдены"}


async def get_all_parsers():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "select * from pay_parsers"
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Парсеры не найдены"}

async def set_parsers(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_string = "SELECT * from pay_parsers where " \
                           "id = " + str(payload.get('id'))
            cur.execute(check_string)
            pars = cur.fetchall()
            if pars:
                data_update = "UPDATE pay_parsers SET "
                for k, v in dict(payload).items():
                    print(k,v)
                    if k != 'id':
                        data_update += str(k) + " = '" + str(v) + "',"
                data_update = data_update[:-1]
                data_update += " where id = " + str(payload.get('id'))
                cur.execute(data_update)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Шаблон изменен"}
                else:
                    return {"Success": False, "data": "Шаблон не изменен"}

            else:
                insert_string = "INSERT INTO pay_parsers (shablon, sender) " \
                                "VALUES ('" + str(payload.get('shablon')) + \
                                "','" + str(payload.get('sender')) + "')"
                cur.execute(insert_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Прасер успешно добавлен"}
                else:
                    return {"Success": False, "data": "Парсер не добавлен"}


async def get_urls_reqs(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select url from pay_reqs_types where id = " + str(id)
            cur.execute(data_check)
            check = cur.fetchone()
            if check:
                return {"Success": True, "data": check['url']}
            else:
                return {"Success": False, "data": "png не найдены"}


async def set_messages(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            message_uuid = await generate_uuid()
            insert_string = "INSERT INTO pay_message (order_uuid, message_uuid, text, docs_url, status, date, email) " \
                            "VALUES ('" + str(payload.order_uuid) + "','" + str(message_uuid) + \
                            "','" + str(payload.text) + "',0,0, UTC_TIMESTAMP(), '"+str(payload.email)+"')"
            cur.execute(insert_string)
            cnx.commit()
            if cur.rowcount > 0:
                result = await send_mail("Ваше обращение по заявке № "+str(message_uuid) + " будет обработано в ближайшее время", "Обращение в службу поддержки", payload.email)
                if result["Success"]:
                    return {"Success": True, "data": message_uuid}
                else:
                    return {"Success": False, "data": "Сообщение не удалось отправить"}
            else:
                return {"Success": False, "data": "Сообщение не отправлено"}


async def insert_check(message_uuid, images):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:

            update_string = "UPDATE pay_message SET docs_url = '" + str(images) + "' where message_uuid = '" + str(message_uuid) +"'"
            cur.execute(update_string)
            cnx.commit()
            if cur.rowcount > 0:
                return {"Success": True, "data": "Добавлен чек"}
            else:
                return {"Success": False, "data": "Платежки не добавлены"}


async def get_messages_by_any(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select * from pay_message where "

            for k, v in dict(payload).items():
                if k != 'id':
                    data_check += "pay_message." + str(k) + " = '" + str(v) + "' and "
            data_check += "pay_message.id > 0"
            cur.execute(data_check)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Сообщения не найдены"}


async def set_message_status(payload):
    with (cpy.connect(**config.config) as cnx):
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select * from pay_message where message_uuid = '" + str(payload.message_uuid) +"'"
            cur.execute(data_check)
            data = cur.fetchone()
            if data:
                update_string = "UPDATE pay_message SET status = " + str(payload.status) + \
                " where message_uuid = '" + str(payload.message_uuid) +"'"
                cur.execute(update_string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Статус сообщения изменен"}
                else:
                    return {"Success": False, "data": "Сообщение не изменено"}
            else:
                return {"Success": False, "data": "Сообщение не найдено"}



async def get_message_url(message_uuid):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select * from pay_message where message_uuid = '" + str(message_uuid) +"'"
            cur.execute(data_check)
            check = cur.fetchone()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Платежка не найдена"}