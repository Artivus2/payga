import re
import datetime
import mysql.connector as cpy
import config
import routers.admin.models as admin_models
from routers.actives.controller import crud_deposit, crud_balance, crud_transfer
from routers.orders.controller import (
    update_order_by_any
)
from routers.orders.utils import get_course
from routers.user.controller import create_random_key
import telebot

#from routers.withdraws.controller import send_to_wallet

botgreenavipay = telebot.TeleBot(config.telegram_api)


async def check_access(request: admin_models.AuthRoles):
    print("user", request)
    if request.user_id != 1:
        return {"Success": False, "data": "Пользователь не имеет прав на выполнение данного метода"}
    return request.user_id
    # user_id_check = False
    #
    # print(user_id, method_id, page_id)
    # with cpy.connect(**config.config) as cnx:
    #     with cnx.cursor() as cur:
    #         data_string = "SELECT FROM user where id = '" + str(user_id) + "'"
    #
    # if user_id_check:
    #     print("тут")
    #     return {"Success": False, "data": "Пользователь не имеет прав на выполнение данного метода"}
    # return {"Success": False, "data": user_id}


async def send_link_to_user(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            try:
                string = "UPDATE user SET banned = 0 where id = '" + str(user_id) + "'"
                cur.execute(string)
                cnx.commit()
                cur.close()
                return {"Success": True, "data": "Пользователь подтвержден"}
            except:
                cur.close()
                return {"Success": False, "data": "Пользователь не подтвержден"}


async def insert_new_user_banned(**payload):
    # try todo
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            app_id = 3  # paygreenavi
            print(payload)
            link_gen = await create_random_key()
            data_login = "SELECT id from user where login = '" + str(payload['login']) + \
                         "' or email = '" + payload['email'] + "'"
            cur.execute(data_login)
            data = cur.fetchone()
            data_ref = "SELECT id from user where affiliate_invitation_code = '" \
                       "" + str(payload['affiliate_invitation_code']) + "'"
            cur.execute(data_ref)
            ref_id = cur.fetchone()
            print("ref_id", ref_id)
            if ref_id:
                ref_id = ref_id['id']
            else:
                ref_id = 0
            if not data:
                banned_for_submit = 1  # блокируем вход до подтверждения админом
                data_string = "INSERT INTO user (login, email, password, affiliate_invitation_id, " \
                              "affiliate_invitation_code, telegram, app_id, banned, role_id) " \
                              "VALUES ('" + str(payload['login']) + "','" + str(payload['email']) + \
                              "','" + str(payload['password']) + "','" + str(ref_id) + "','" + str(link_gen)\
                              + "','" + str(payload['telegram']) + "','" + str(app_id) + "','" \
                              + str(banned_for_submit) + "', 0)"
                cur.execute(data_string)
                cnx.commit()
                data_user_id = "SELECT * from user where login = '" + str(payload['login']) + \
                               "' and email = '" + payload['email'] + "'"
                cur.execute(data_user_id)
                data_user = cur.fetchone()
                if data_user and ref_id != 0:
                    # insert refs
                    pay_refs = "INSERT INTO pay_refs (user_id, referal_id, level) " \
                               "VALUES ('" + str(data_user['id']) + "','" + str(ref_id) + "', '0')"
                    cur.execute(pay_refs)
                    cnx.commit()
                cnx.close()
                # print(comment)
                message = "Пользователь " + str(payload['email']) \
                          + " поставлен в очередь на регистрацию " + str(datetime.utcnow())
                botgreenavipay.send_message(config.pay_main_group, message)
                return {"Success": True, "data": "Поставлен в очередь на регистрацию. Ожидайте"}
            else:
                return {"Success": False, "data": "Пользователь: " + str(payload['email'])
                                                  + ' / ' + str(payload['login']) + " уже существует"}


async def get_all_users_profiles(payload):
    """
    получаем все данные пользователей
    :param user_id:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT user.id, login, role_id, email, phone, " \
                     "telegram, created_at as reg_date, telegram_connected, " \
                     "twofa_status, user.verify_status, verify_status.title as verify, user.banned as banned_status," \
                     "banned_status.title as banned, user.chart_id, chart.symbol as chart, user.currency_id, " \
                     "is_active, is_admin, affiliate_invitation_code, " \
                     "currency.symbol as currency from user " \
                     "LEFT JOIN verify_status ON user.verify_status = verify_status.id " \
                     "LEFT JOIN banned_status ON user.banned = banned_status.id " \
                     "LEFT JOIN chart ON user.chart_id = chart.id " \
                     "LEFT JOIN currency ON user.currency_id = currency.id " \
                     "where "
            id = payload.get('id', 0)
            if id > 0:
                for k, v in dict(payload).items():
                    string += "user." + str(k) + " = '" + str(v) + "' and "
                string += "user.id is not null"
            else:
                for k, v in dict(payload).items():
                    if k != 'id':
                        string += "user." + str(k) + " = '" + str(v) + "' and "
                string += "user.id is not null"
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Данных нет"}


async def get_all_roles(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_admin_roles"
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Роли не доступны или не найдены"}


async def crud_roles(crud, payload):  # todo -> admin
    """
    id: int | None = None
    title: str | None = None
    pages: int | None = None
    status: int | None = None
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if crud == 'create':
                data_string = "INSERT INTO pay_admin_roles (title, pages, status) " \
                              "VALUES ('" + str(payload.title) + "','" + str(payload.pages) + "','1')"
                try:
                    cur.execute(data_string)
                    cnx.commit()
                    return {"Success": True, "data": "Роль создана"}
                except:
                    return {"Success": False, "data": "Роль не создана"}
            if crud == 'set':
                string = "UPDATE pay_admin_roles set title = '" + str(payload.title) + \
                         "' where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Роль Успешно изменена"}
                else:
                    cnx.close()
                    return {"Success": True, "data": "Не удалось изменить роль"}
            if crud == 'remove':
                string = "UPDATE pay_admin_roles set status = 0 " \
                         "where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    cnx.close()
                    return {"Success": True, "data": "Роль успешно удалена. не действует"}
                else:
                    cnx.close()
                    return {"Success": True, "data": "Не удалось удалить"}
            if crud == 'status':
                string = "UPDATE pay_admin_roles set status = '" + str(payload.status) \
                         + "' where id = " + str(payload.id)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    return {"Success": True, "data": "Статус изменен"}
                else:
                    return {"Success": False, "data": "Не удалось изменить статус"}
    return {"Success": False, "data": "Операцию провести не удалось"}


async def change_user_role(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE user SET role_id = " + str(payload.role_id) + " where id = " + str(payload.user_id)
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                return {"Success": True, "data": "Роль изменена"}
            else:
                return {"Success": False, "data": "Не удалось изменить роль пользователя"}


async def set_users_any(payload):  # эталон для update
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_update = "UPDATE user SET "
            for k, v in dict(payload).items():
                if k != 'user_id':
                    data_update += str(k) + " = '" + str(v) + "',"
            data_update = data_update[:-1]
            data_update += " where id = " + str(payload.get('user_id'))
            try:
                cur.execute(data_update)
                cnx.commit()
            except:
                cnx.close()
                return {"Success": False, "data": "Не корректные данные"}
            if cur.rowcount > 0:
                cnx.close()
                return {"Success": True, "data": "Успешно обновлены реквизиты пользователя"}
            else:
                cnx.close()
                return {"Success": False, "data": "реквизиты пользователя не обновлены"}



async def get_is_active(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT is_active from user where id = " + str(user_id)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return data['is_active']
            else:
                return False


async def create_sms_data(payload):
    """
    первично собрали данные по api_key в pay_sms_data
    :param payload:
    :return:
    'user_id_trader': user_id_trader,
                'sender': sender,
                'sum_fiat': suma,
    """
    user_id_trader = payload.get('user_id_trader')
    sum_fiat = float(payload.get('sum_fiat'))
    low = sum_fiat - 1
    high = sum_fiat + 1

    #check_active = await get_is_active(user_id)
    #if check_active:
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # проверить включена ли автотматика на группу todo

            check_string = "SELECT id, uuid, sum_fiat, user_id, user_pay, date_expiry FROM pay_orders " \
                           "where user_id = '" \
                           + str(user_id_trader) + "' and pay_notify_order_types_id = 0 and sum_fiat >= '"\
                           + str(low) + "' and sum_fiat <= '"+str(high)+"'"
            print(check_string)
            cur.execute(check_string)
            data = cur.fetchone()
            if data:
                # проверяем ордер пришло зачисление
                print(data)
                if data['date_expiry'] > datetime.datetime.utcnow(): #срок не вышел
                    #USDT отправляет автоматика
                    print("sms",data)

                    data_string = "INSERT INTO pay_sms_data (user_id, date, sum_fiat, sender, text) " \
                                  "VALUES ('" + str(payload.get('user_id_trader')) + "','" + str(
                        payload.get('datain')) \
                                  + "','" + str(payload.get('sum_fiat')) + "','" + str(payload.get('sender')) \
                                  + "','" + str(payload.get('text')) + "')"
                    cur.execute(data_string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        message = "Ордер " + str(data['uuid']) + " \nполучен платеж на сумму " \
                                  + str(payload.get('sum_fiat')) + "\nОбработано автоматикой\n" \
                                  + str(payload.get('text')) + "\n"
                        botgreenavipay.send_message(config.pay_main_group, message)
                        payed = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 3})
                        if payed["Success"]:
                            #принят оплачен
                            return {"Success": True, "data": 'ордер принят и оплачен'}
                        else:
                            return {"Success": False, "data": 'Ордер не оплачен'}
                    else:
                        return {"Success": False, "data": 'Данные не добавлены'}
                else:
                    print('ордер просрочен')
                    #await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 5})
                    return {"Success": False, "data": 'Автоматизация не проведена, ордер просрочен'}
            else:
                print('#ордер не найден или сумма не точная')
                #await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 5})
                return {"Success": False, "data": 'Автоматизация не проведена, не найден ордер'}


async def check_order_by_id_payin(payload):
    """
    проверка ордеров админом менеджером
    :param payload:
    :return:
    """
    order_id = payload.id #todo pay_notify_order_types_id
    notify = payload.pay_notify_order_types_id
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_orders where id = '" + str(order_id) \
                     + "' and pay_id = 1"
            cur.execute(string)
            data = cur.fetchone()
            print(data)
            if data:
                value = data.get('value')
                # переводим value из pay_orders

                transfer = {
                    'user_id_in': data.get('user_pay'),
                    'user_id_out': data.get('user_id'),
                    'value': value
                }
                if notify == 3:
                    result = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': notify})
                    # получили данные по ордеру
                    if result:
                        return {"Success": True, "data": "Средства отправлены мерчанту"}
                    else:
                        return {"Success": False, "data": "Статус не изменен"}

                elif notify == 2:

                    result = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': notify})
                    if result["Success"]:
                        return {"Success": True, "data": "Ордер отменен"}
                    else:
                        return {"Success": True, "data": "Ордер не отменен"}



                elif notify == 4:
                    print("ордер оплачен, время еще не вышло но не сработала автоматика")
                elif notify == 5:
                    print("чек не соответствует, оплата не проведена, переведен в диспут")
                else:
                    return {"Success": False, "data": "Не верно указан статус PAYIN ордера"}
            else:
                return {"Success": False, "data": "Ордер не найден"}


async def check_order_by_id_payout(payload):
    """
    проверка ордеров админом менеджером
    :param payload:
    :return:
    """
    order_id = payload.id
    notify = payload.pay_notify_order_types_id
    print(order_id)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_orders where id = '" + str(order_id)\
                     + "' and pay_id = 2 and pay_notify_order_types_id = 18"
            cur.execute(string)
            data = cur.fetchone()
            print(data)
            if data:
                if int(notify) == 21:
                    result = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': notify})
                    # send usdt auto
                    return {"Success": True, "data": "Ордер подтвержден"}
                elif int(notify) == 20:
                    result = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': notify})
                    return {"Success": True, "data": "Ордер отменен"}
                else:
                    return {"Success": False, "data": "Не верно указан статус PAYOUT ордера"}
            else:
                return {"Success": False, "data": "Ордер не найден"}





async def get_user_from_api_key(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:

            string = "SELECT user_id from pay_api_keys where " \
                     "api_key_expired_date > UTC_TIMESTAMP() and " \
                     "status in (0,1,3) and api_key = '" + str(payload) + "'"
            cur.execute(string)
            data = cur.fetchone()
            print(data)
            if data:
                return {"Success": True, "data": data.get('user_id')}
            else:
                return {"Success": False, "data": 'api_key не найден'}


async def get_info_for_invoice(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # достаем типы оплаты
            select_reqs = "SELECT id, title, url from pay_reqs_types"
            cur.execute(select_reqs)
            datareqs = cur.fetchall()
            if datareqs: # для перавой страниц сбп с карты на карту
                all = []
                for types_reqs in datareqs:

                    result0 = {
                        "id": types_reqs.get('id'),
                        "title": types_reqs.get('title'),
                        "url": types_reqs.get('url')
                    }
                    string2 = "SELECT pay_pay_percent.value as cashback, pay_reqs.id as req_id, pay_reqs.value, pay_reqs.fio, pay_admin_banks.title as bank_title, "+\
                              "pay_admin_banks.id as bank_id, pay_admin_banks.url as bank_url FROM pay_reqs " + \
                              "LEFT JOIN user ON user.id = pay_reqs.user_id " + \
                              "LEFT JOIN pay_pay_percent ON pay_pay_percent.user_id = pay_reqs.user_id and pay_pay_percent.pay_id = 1 " + \
                              "LEFT JOIN pay_fav_banks ON pay_reqs.bank_id = pay_fav_banks.id " + \
                              "LEFT JOIN pay_admin_banks ON pay_fav_banks.bank_id = pay_admin_banks.id " + \
                              "WHERE reqs_types_id = '" + str(types_reqs.get('id')) + \
                               "' and reqs_status_id = 1 and pay_pay_id = 1 and user.role_id = 4 and user.app_id = 3 ORDER BY RAND() LIMIT 1"
                    cur.execute(string2)
                    data2 = cur.fetchall()
                    if data2:
                        for x in data2:
                            check_reqs_limits = await get_reqs_limits_by_req_id(x.get('req_id'))
                            if check_reqs_limits:
                                print(data2)
                                result0["reqs"] = data2


                            else:
                                result0["reqs"] = []
                    else:
                        result0["reqs"] = []
                    all.append(result0)
                if len(all) > 0:
                    return {"Success": True, "data": all}
                else:
                    return {"Success": False, "data": "Реквизиты не найдены, попробуйте позже"}
            else:
                return {"Success": False, "data": "Нет доступных иетодов оплаты"}


async def get_reqs_limits_by_req_id(req_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            if req_id > 0:
                # todo проверить занятость в ордерах со статусом не 3
                # по sequence, qty_limit_hour, qty_limit_day qty_limit_month sum_limit_hour sum_limit_day sum_limit_month limit_active_orders
                string_reqs = "SELECT * from pay_reqs where id = " + str(req_id)
                cur.execute(string_reqs)
                data0 = cur.fetchone()
                if data0:

                    limit_active_orders = data0.get('limit_active_orders')
                    string = "SELECT count(*) as active_orders FROM pay_orders where pay_notify_order_types_id = 0 and req_id = " + str(req_id)
                    cur.execute(string)
                    data = cur.fetchone()
                    if data:
                        active_orders_by_req = data.get('active_orders')
                        if limit_active_orders >= active_orders_by_req:
                            print("limit_active_orders", limit_active_orders, "active_orders_by_req", active_orders_by_req)
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False



async def get_trader_user_id(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # ищем reqs_group_id формируем список из доступных банков
            print(payload)
            string = "SELECT user_id FROM pay_reqs where id = " + str(payload)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return data.get('user_id')
            else:
                return 0

def get_pattern_from_bd(sender):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # ищем reqs_group_id формируем список из доступных банков
            string = "SELECT shablon FROM pay_parsers where sender = '" + str(sender) + "'"
            cur.execute(string)
            data = cur.fetchall()
            print("parsers", data)
            if data:
                return data
            else:
                return False

async def get_pattern(sender, text):
    """

    :return:
    """
    matches = None
    parsers = get_pattern_from_bd(sender)
    if parsers:
        for i in parsers:
            matches = re.search(i["shablon"], text, re.VERBOSE)
            if matches:
                print("совпадение найдено,", matches)
                break
        if matches:
            suma = matches.group(1).split(" ")
            #title = get_bank_id(sender) # todo сравнить sender и title bank у user
            result = {
                'Success': True,
                'sender': sender,
                'sum_fiat': float(suma[0]),
                'datain': datetime.datetime.utcnow(),
                'text': text,
             #   'bank_id': bank_id
            }
            return result
        else:
            return {'Success': False}
    else:
        return {'Success': False}


async def confirm_balance_to_network(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            history_check = "select id from pay_deposit_history where status_id = 0 " \
                            "and user_id = " + str(payload.user_id)
            cur.execute(history_check)
            data0 = cur.fetchone()
            if data0:
                check_string = "SELECT value, withdrawals FROM pay_balance where baldep_status_id = 1 " \
                               "and baldep_types_id = 1 and " \
                               "withdrawals > 0 and user_id = " + str(payload.user_id)
                cur.execute(check_string)
                data = cur.fetchone()
                if data:
                    value = data.get('withdrawals')
                    update_balance = "UPDATE pay_balance set withdrawals = 0 where user_id = " + str(payload.user_id)
                    cur.execute(update_balance)
                    cnx.commit()
                    if cur.rowcount > 0:
                        # todo add status to history
                        result = await set_deposit_history_status(data0.get('id'), 1)
                        if result:
                            #send transaction to trx
                            wallet = "UBObjOBb"

                            return {"Success": True, "data": str(value) + ' USDT отправлено на кошелек: ' + str(wallet)}
                        else:
                            return {"Success": False, "data": 'Не удалось отправить средства. Обратитесь к администратору'}
                else:
                    return {"Success": False, "data": 'Недостаточно средств на балансе'}
            else:
                return {"Success": False, "data": "Заявка не найдена. Обратитесь к администратору"}

async def confirm_deposit_to_balance(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            find_history = "select id from pay_deposit_history where status_id = 3 " \
                           "and user_id = " + str(payload.user_id)
            cur.execute(find_history)
            data0 = cur.fetchone()
            if data0:
                if payload.status_id == 1:
                    check_string = "SELECT withdrawals FROM pay_deposit where baldep_status_id = 1 and baldep_types_id = 1 and " \
                                   "withdrawals > 0 and user_id = " + str(payload.user_id)
                    cur.execute(check_string)
                    data = cur.fetchone()
                    if data:
                        check_balance = "SELECT value from pay_balance where baldep_status_id = 1 and baldep_types_id = 1 and " \
                                        "user_id = " + str(payload.user_id)
                        cur.execute(check_balance)
                        data_bal = cur.fetchone()
                        if not data_bal:
                            return {"Success": False, "data": 'Вывод не может быть осуществлен'}
                        else:
                            current_value = data_bal.get('value',0)
                            update_balance = "UPDATE pay_balance set value = '" +str(current_value + data.get('withdrawals')) + "' " \
                                             "where user_id = " + str(payload.user_id)
                            cur.execute(update_balance)
                            cnx.commit()
                            if cur.rowcount > 0:
                                update_deposit = "UPDATE pay_deposit set withdrawals = 0 " \
                                                 "where user_id = " + str(payload.user_id)
                                cur.execute(update_deposit)
                                cnx.commit()
                                if cur.rowcount > 0:
                                    result = await set_deposit_history_status(data0.get('id'), 1)
                                    print(result)
                                    if result:
                                        return {"Success": True, "data": 'Вывод с депозита подтвержден. Оформляйте заявку на вывод с баланса'}
                                    else:
                                        return {"Success": False, "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
                            else:
                                return {"Success": False, "data": 'Не удалось обновить баланс. Обратитесь к администратору'}
                    else:
                        return {"Success": False, "data": 'Не найдены параметры баланса. Обратитесь к администратору'}
                if payload.status_id == 2:
                    check_string = "SELECT value, withdrawals FROM pay_deposit where baldep_status_id = 1 and baldep_types_id = 1 and " \
                                   "withdrawals > 0 and user_id = " + str(payload.user_id)
                    cur.execute(check_string)
                    data = cur.fetchone()
                    if data:
                        current_value = data.get('value')
                        current_withdrawals = data.get('withdrawals')
                        update_deposit = "UPDATE pay_deposit set withdrawals = 0, value = " + str(current_value + current_withdrawals) + \
                                         "where user_id = " + str(payload.user_id)
                        cur.execute(update_deposit)
                        cnx.commit()
                        if cur.rowcount > 0:
                            return {"Success": True,
                                    "data": 'Вывод с депозита отменен'}
                        else:
                            return {"Success": False,
                                    "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
                    else:
                        return {"Success": False,
                                "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
            else:
                return {"Success": False, "data": "Заявка не найдена. Обратитесь к администратору"}

async def confirm_bal_or_dep_funds(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            find_history = "select id, value from pay_deposit_history where status_id = 6 " \
                           "and user_id = " + str(payload.user_id)
            cur.execute(find_history)
            data0 = cur.fetchone()
            if data0:
                check_deposit = "SELECT * from pay_deposit where baldep_status_id = 1" \
                                " and baldep_types_id = 1 and " \
                                "user_id = " + str(payload.user_id)
                cur.execute(check_deposit)
                data = cur.fetchone()
                if data:
                    min_deposit = float(data.get('min_deposit')) #2000
                    value = float(data0.get('value')) #на сколько пополняем 2000
                    deposit_current_value = float(data.get('value')) #1900

                    check_balance = "SELECT * from pay_balance where baldep_status_id = 1" \
                                    " and baldep_types_id = 1 and " \
                                    "user_id = " + str(payload.user_id)
                    cur.execute(check_balance)
                    data_bal = cur.fetchone()
                    if not data_bal:
                        return {"Success": False, "data": "Параметры баланса не определены. Обратитесь к администратору"}
                    else:
                        # добавляем баланс и депозит
                        balance_current_value = float(data_bal.get('value')) #4000
                        if deposit_current_value < min_deposit:
                            if value <= min_deposit - deposit_current_value:
                                payload.value = deposit_current_value + value
                                result_dep = await crud_deposit("set", payload)
                                if result_dep["Success"]:
                                    if cur.rowcount > 0:
                                        result = await set_deposit_history_status(data0.get('id'), 4)
                                        print(result)
                                        if result:
                                            return {"Success": True, "data": "Депозит и баланс изменены"}
                                        else:
                                            return {"Success": False,
                                                    "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
                            else:
                                payload.value = balance_current_value + value - min_deposit + deposit_current_value
                                result_bal = await crud_balance("set", payload)
                                if result_bal["Success"]:
                                    payload.value = min_deposit
                                    result_dep = await crud_deposit("set", payload)
                                    if result_dep["Success"]:
                                        result = await set_deposit_history_status(data0.get('id'), 4)
                                        if result:
                                            return {"Success": True, "data": "Баланс пополнен"}
                                        else:
                                            return {"Success": False,
                                                    "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
                                    else:
                                        return {"Success": False,
                                                "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
                                else:
                                    return {"Success": False,
                                            "data": 'Не удалось обновить баланс. Обратитесь к администратору'}
                        else:
                            payload.value = balance_current_value + value
                            result_bal = await crud_balance("set", payload)
                            if result_bal["Success"]:
                                if cur.rowcount > 0:
                                    result = await set_deposit_history_status(data0.get('id'), 4)
                                    print(result)
                                    if result:
                                        return {"Success": True, "data": "Баланс пополнен. Депозит соответствует минимальному"}
                                    else:
                                        return {"Success": False,
                                                "data": 'Не удалось обновить депозит. Обратитесь к администратору'}
                else:
                    return {"Success": False, "data": "Баланс не активирован. Обратитесь к администратору"}
            else:
                return {"Success": False, "data": "Не найдена заявка на пополнение. Обратитесь к администратору"}


async def set_deposit_history_status(id, status):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            find_history_withdrawals = "select * from pay_deposit_history where id = " + str(id)
            cur.execute(find_history_withdrawals)
            data = cur.fetchone()
            if data:
                update_history = "UPDATE pay_deposit_history set status_id = '"+str(status)+"'" \
                                 " where id = " + str(id)
                cur.execute(update_history)
                cnx.commit()
                if cur.rowcount > 0:
                    return True
                else:
                    return False
            else:
                return False


async def get_payout_status(order_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            check_order = "SELECT uuid, pay_notify_order_types_id, value, user_pay, DATE_FORMAT(pay_orders.date_expiry, " \
                          + str(config.date_format_all) + ") as date_expiry, o_id FROM pay_orders where o_id = '" + str(
                order_id) + "'"
            cur.execute(check_order)
            data = cur.fetchone()
            print(data)
            if data:
                result = {
                    'status': data.get('pay_notify_order_types_id'),
                    'value': data.get('value'),
                    'order_uuid': data.get('uuid'),
                    'merchant_id': data.get('user_pay'),
                    'date_expiry': data.get('date_expiry'),
                    'o_id': data.get('o_id')
                }
                if result.get('status') == 0:  # todo
                    result["status_title"] = "Ожидает оплаты"
                    return {"Success": True, "data": result}
                elif result.get('status') == 15:
                    result["status_title"] = "Оплачен"
                    return {"Success": True, "data": result}
                elif result.get('status') == 20:
                    result["status_title"] = "Отменен"
                    return {"Success": True, "data": result}
                elif result.get('status') == 21:
                    result["status_title"] = "Успешно проведен"
                    return {"Success": True, "data": result}
                else:
                    return {"Success": False, "data": "не удалось найти данные"}
            else:
                return {"Success": False, "data": "не удалось найти ордер"}

async def get_payment_status(uuids):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            """
            waiting - waiting for the customer to send the payment. The initial status of each payment;
            confirming - the transaction is being processed on the blockchain. Appears when pay.greenavi.com
                        detect the funds from the user on the blockchain;
            confirmed - the process is confirmed by the blockchain. Customer’s funds have accumulated enough confirmations;
            sending - the funds are being sent to your personal wallet. We are in the process of sending the funds to you;
            finished - the funds have reached your personal address and the payment is finished;
            failed - the payment wasn't completed due to the error of some kind;
            refunded - the funds were refunded back to the user;
            expired - the user didn't send the funds to the specified address in the 7 days time window;
            """
            check_order = "SELECT id, uuid, pay_notify_order_types_id, value, user_pay, DATE_FORMAT(pay_orders.date_expiry, " \
                          + str(config.date_format_all)+") as date_expiry, o_id FROM pay_orders where uuid = '" + str(uuids) + "'"
            cur.execute(check_order)
            data = cur.fetchone()
            print(data)
            if data:
                result = {
                    'id': data.get('id'),
                    'status': data.get('pay_notify_order_types_id'),
                    'value': data.get('value'),
                    'order_uuid': data.get('uuid'),
                    'merchant_id': data.get('user_pay'),
                    'date_expiry': data.get('date_expiry'),
                    'o_id': data.get('o_id')
                }
                if result.get('status') == 0: #todo
                    result["status_title"] = "Ожидает оплаты"
                    return {"Success": True, "data": result}
                elif result.get('status') == 1:
                    result["status_title"] = "Оплачен"
                    return {"Success": True, "data": result}
                elif result.get('status') == 2:
                    result["status_title"] = "Отменен"
                    return {"Success": True, "data": result}
                elif result.get('status') == 3:
                    result["status_title"] = "Успешно проведен"
                    return {"Success": True, "data": result}
                else:
                    return {"Success": False, "data": "не удалось найти данные"}
            else:
                return {"Success": False, "data": "не удалось найти ордер"}


async def get_data_sms(payload):
    with (cpy.connect(**config.config) as cnx):
        with cnx.cursor(dictionary=True) as cur:
            check_order = "SELECT * FROM pay_sms_data where user_id = '" + str(payload) + "'"
            cur.execute(check_order)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Данные не найдены"}


async def get_active_traders(payload):
    with (cpy.connect(**config.config) as cnx):
        with cnx.cursor(dictionary=True) as cur:
            check_order = "SELECT user.id, login, email FROM user " + \
                          "LEFT JOIN pay_reqs ON user.id = pay_reqs.user_id " + \
                          "where is_active = 1 and role_id = 4 and banned = 0 and pay_reqs.pay_pay_id = 2 " + \
                          " and reqs_status_id = 1"
            cur.execute(check_order)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Данные не найдены"}



async def set_admin_banks_png(id, images):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            #for i in images:
            string_check = "select * from pay_admin_banks where order_id = " + str(id)
            cur.execute(string_check)
            data = cur.fetchall()
            if not data:
                insert_string = "INSERT into pay_admin_banks (id, url) " \
                              "VALUES ('" + str(id) + "','" + str(images) + "')"
                cur.execute(insert_string)
                cnx.commit()
            else:
                update_string = "UPDATE pay_admin_banks SET url = '" + str(images) + "' where id = " + str(id)
                cur.execute(update_string)
                cnx.commit()
            if cur.rowcount > 0:
                string_check = "select id from pay_admin_banks where id = " + str(id)
                cur.execute(string_check)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data[0].get('id')}
                else:
                    return {"Success": False, "data": "png не добавлены"}


async def set_reqs_png(id, images):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            #for i in images:
            string_check = "select * from pay_reqs_types where id = " + str(id)
            cur.execute(string_check)
            data = cur.fetchall()
            if not data:
                insert_string = "INSERT into pay_reqs_types (id, url) " \
                              "VALUES ('" + str(id) + "','" + str(images) + "')"
                cur.execute(insert_string)
                cnx.commit()
            else:
                update_string = "UPDATE pay_reqs_types SET url = '" + str(images) + "' where order_id = " + str(id)
                cur.execute(update_string)
                cnx.commit()
            if cur.rowcount > 0:
                string_check = "select id from pay_reqs_types where id = " + str(id)
                cur.execute(string_check)
                data = cur.fetchall()
                if data:
                    return {"Success": True, "data": data[0].get('id')}
                else:
                    return {"Success": False, "data": "png не доюавлены"}