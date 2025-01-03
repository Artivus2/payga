import re
import datetime
from cgi import print_form

import mysql.connector as cpy

import config
import routers.admin.models as admin_models
from routers.actives.controller import crud_deposit, crud_balance, crud_transfer
from routers.orders.controller import (
    create_order_for_user,
    update_order_by_any
)
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


async def create_invoice_data(payload):
    """
    Создание ордера payin на основе данных из смс и выбора пользователя
    1) #из окна приема платежа выбирают мои доступные реквизиты (сбер, открытие, райффазен)
    2) # из имеющихся доступных реквизитов сбера/открытия/райффайзен выбираем подходящий по доступности, параметрам и лимитам
    3) # по факту это create-invoice со стороны магазина (от туда мы получаем выбраные req_group_id, sum_fiat, bank_id (из fav_bank)
     из формы ввода суммы и выбора банка)
    4) # создаем ордер payin (
    uuid: генерится
    user_id: по api_key магазина достать из базы данных,
    course: - текущий USDT с coinbase к payload.valuta,
    chart_id - по умолчанию USDT (259)
    sum_fiat - payload.suma по поступлению смс об оплате после парсинга
    pay_id: 1 - payin
    value: sum_fiat / course - количество USDT на отправку мерчанту на счет - cashback % (pay_pay_percent)
    date: дата полуения смс, создания ордера по факту
    date_expiry: +15 минут от date
    req_id: из invoice
    pay_notify_order_types_id: 1 - статус ордер создан
    docs_id: путь к прикрепленному чеку об оплате
    )
     5) # ждем оплаты со стороны покупателя в течении 15 минут (ждем /sms-data)
    6) # по bank_id выбираем соответствующую строку парсера
    7) # ожидаем оплаты и прихода смс
    8) если рубли по факту пришли за 15 минут, нажимаем подтвердить ордер. статус успешно. отправка usdt мерчанту
       если рубли не пришли в течение 15 минут на кроне ордер уйдет в отмену.
       если рубли пришли после 15 минут достаем из отмены в успех руками. отправка usdt мерчанту

    :param payload:
    :return:
    """
    # data_normalize = payload.get('datain')
    user_sender = await get_user_from_api_key(payload.api_key)
    result_from_invoice = {
        "req_id": payload.req_id,
        "sum_fiat": payload.sum_fiat,
        'user_id': user_sender['data'],
        'pay_id': 1
    }
    response = await create_order_for_user(result_from_invoice)
    print(response)
    return response


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
    'user_id_merchant': user_id_merchant,
                'sender': sender,
                'sum_fiat': suma,
    """

    user_id_merchant = payload.get('user_id_merchant', 0)
    #check_active = await get_is_active(user_id)
    #if check_active:
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # проверить включена ли автотматика на группу todo

            check_string = "SELECT id, uuid, sum_fiat, user_id, user_pay, date_expiry FROM pay_orders " \
                           "where user_pay = '" \
                           + str(user_id_merchant) + "' and pay_notify_order_types_id = 0 and sum_fiat = '"\
                           + str(payload.get('sum_fiat', 0)) + "'"
            cur.execute(check_string)
            data = cur.fetchone()
            if data:
                # проверяем ордер пришло зачисление

                if data['date_expiry'] > datetime.datetime.utcnow(): #срок не вышел
                    #USDT отправляет автоматика
                    print("sms",data)

                    data_string = "INSERT INTO pay_sms_data (user_id, date, sum_fiat, sender, text) " \
                                  "VALUES ('" + str(payload.get('user_id_merchant')) + "','" + str(
                        payload.get('datain')) \
                                  + "','" + str(payload.get('sum_fiat')) + "','" + str(payload.get('sender')) \
                                  + "','" + str(payload.get('text')) + "')"
                    cur.execute(data_string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        message = "Ордер " + str(data['uuid']) + " \nполучен платеж на сумму " \
                                  + str(payload.get('sum_fiat')) + "\nОбработано автоматикой\n" \
                                  + str(payload.get('text')) + "\n"
                        # botgreenavipay.send_message(config.pay_main_group, message)
                        payed = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 1})
                        if payed["Success"]:
                            #принят оплачен
                            return {"Success": True, "data": 'ордер принят и оплачен'}
                        else:
                            return {"Success": False, "data": 'Ордер не оплачен'}
            else:
                #ордер не найден или сумма не точная
                await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 5})
                return {"Success": False, "data": 'Автоматизация не проведена, ордер переведен в диспут'}

                # else:
                #     # USDT не удалось отправить, ручная отправка
                #     await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 4})
                #     return {"Success": False, "data": 'не удалось отправить USDT, ручная отправка'}
            # else:
            #     await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 8})
            #     return {"Success": False,
            #             "data": 'не найден кошелек или не активирован, обратитесь к администратору'}
            #     else:
            #         #ордер просрочен переведен в диспут
            #         await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': 8})
            #         return {"Success": False, "data": 'sms data не добавлена, ордер просрочен'}




async def check_order_by_id_payin(payload):
    """
    проверка ордеров админом менеджером
    :param payload:
    :return:
    """
    order_id = payload.id
    notify = payload.pay_notify_order_types_id
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_orders where id = '" + str(order_id) \
                     + "' and pay_id = 1 and pay_notify_order_types_id = 5"
            cur.execute(string)
            data = cur.fetchone()
            print(data)
            if data:
                if notify == 3:
                    result = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': notify})
                    # получили данные по ордеру
                    if result:
                        #переводим value из pay_orders

                        transfer = {
                            'user_id_in': data.get('user_pay'),
                            'user_id_out': data.get('user_id'),
                            'value': data.get('value')
                        }
                        send = crud_transfer("payin", transfer)
                        if send["Success"]:
                            return {"Success": True, "data": "Средства отправлены мерчанту"}
                        else:
                            return {"Success": True, "data": "Средства не отправлены"}
                elif notify == 2:
                    result = await update_order_by_any({'id': data.get('id'), 'pay_notify_order_types_id': notify})
                    return {"Success": True, "data": "Ордер отменен"}
                elif notify == 3:
                    print("ордер успешный PAYIN, отправили USDT на баланс мерчанту")
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
            #достаем user_id мерчанта из апи кей
            data0 = await get_user_from_api_key(payload)

            if data0:
                user_id_merchant = data0.get('data')
                # в кабине мерчанта смотрим активные банки для приема платежей от пользователей из fav_banks id
                select_banks = "SELECT bank_id from pay_fav_banks where active = 1 and user_id = " + str(user_id_merchant)
                cur.execute(select_banks)
                merch_banks = cur.fetchall()
                if merch_banks:
                    banks = []
                    if len(merch_banks) > 1:
                        for i in merch_banks:
                            banks.append(i.get('bank_id'))
                        banks = "in " + str(tuple(banks))
                    else:
                        banks = "= " + str(merch_banks[0].get('bank_id'))
                    all = []
                    # #ищем доступных трейдеров по bank_id мерча
                    traders = "SELECT pay_reqs_groups.id as pay_reqs_groups_id, " \
                              "pay_reqs_groups.title as pay_reqs_groups_title from user " \
                              "LEFT JOIN pay_reqs ON user.id = pay_reqs.user_id " \
                              "LEFT JOIN pay_reqs_groups ON pay_reqs.req_group_id = pay_reqs_groups.id " \
                              "where user.is_active = 1 and pay_reqs.req_group_id > 0 and " \
                              "pay_reqs.pay_pay_id = 1 " \
                              "and pay_reqs.reqs_status_id = 1 and " \
                              "user.role_id = 4 and pay_reqs.bank_id " + str(banks)\
                              + " group by pay_reqs_groups.id"
                    cur.execute(traders)
                    avail_traders = cur.fetchall()
                    for j in avail_traders:
                        result = {}
                        result["id"] = j.get('pay_reqs_groups_id')
                        result["title"] = j.get('pay_reqs_groups_title')
                        #todo проверить занятость в ордерах со статусом не 3
                        string2 = "SELECT * FROM pay_reqs where req_group_id = '" + str(j.get('pay_reqs_groups_id')) \
                                  + "' and reqs_status_id = 1 and pay_pay_id = 1"
                        cur.execute(string2)
                        data2 = cur.fetchall()
                        if data2:
                            result["reqs"] = data2
                        else:
                            result["reqs"] = []
                        all.append(result)
                    print(len(all))
                    if len(all) >0:
                        return {"Success": True, "data": all}
                    else:
                        return {"Success": False, "data": "Реквизиты не найдены, попробуйте позже"}
            else:
                return {"Success": False, "data": "запрос не действителен. Обратитесь к администратору"}

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

async def get_pattern(sender, text):
    """

    :return:
    """
    matches = None
    parsers = get_pattern_from_bd(sender)
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
            find_history = "select id from pay_deposit_history where status_id = 0 " \
                           "and user_id = " + str(payload.user_id)
            cur.execute(find_history)
            data0 = cur.fetchone()
            if data0:
                check_string = "SELECT withdrawals FROM pay_deposit where baldep_status_id = 1 and baldep_types_id = 1 and " \
                               "withdrawals > 0 and user_id = " + str(payload.user_id)
                cur.execute(check_string)
                data = cur.fetchone()
                if data:
                    check_balance = "SELECT value from pay_balance where baldep_status_id = 1 and baldep_types_id = 1 and " \
                                    "user_id = " + str(payload.user_id)
                    cur.execute(check_balance)
                    data_bal = cur.fetchone()
                    print(data_bal)
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