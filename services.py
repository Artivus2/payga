import datetime
import random
import uuid
import mysql.connector as cpy
import requests
from fastapi import HTTPException

import config
import telebot

botgreenavipay = telebot.TeleBot(config.telegram_api)


# check_orders
def check_orders():
    """
    (/set-order-status)
    '0', 'не принятые ордера'
    '1', 'Получен ордер', '1' /create-order +
    '2', 'Ордер отменен', '1' /order-cancel
    '3', 'Ордер переведен в успех', '1' manual /order-success
    '4', 'Ордер оплачен клиентом', '1' manual /order-payed
    '5', 'Ордер переведен в диспут', '1' manual /order-disput
    '6', 'Ордер создан менеджером и переведен в диспут', '1' /order-manager-created
    '7', 'Успешный ордер переведен в отмену', '1' manual /order-cancel-confirmed из 3 в 2
    '8', 'Ордер переведен в диспут. Закончилось Время (utc) подтверждения оплаты', '1' 4 -15 минут AUTO из 4
    '9', 'Ордер отменен. Закончилось Время (utc) подтверждения оплаты', '1' 4 -15 минут AUTO из 1
    '10', 'Ордер подтвержден автоматикой', '1' /order-auto-confirmed
    '11', 'Ордер переведен из диспута в успех', '1' manual 8 -> 3 /order-confirmed
    '12', 'Ордер переведен из диспута в отмену', '1' manual 8 -> 2 /order-canceled
    '13', 'Реквизиты заблокированы', '1' manual /order-block-reqs
    '14', 'Реквизиты разблокированы', '1' manual /order-unblock-reqs

    '0', 'не принятые ордера'
    '15', 'Получен ордер', '2'
    '16', 'Закончилось Время (utc) подтверждения принятия', '2' 240 минут в 0
    '17', 'Закончилось Время (utc) подтверждения оплаты', '2' сколько времени
    '18', 'Ордер переведен в диспут', '2'
    '19', 'Ордер создан менеджером и переведен в диспут', '2'
    '20', 'Ордер отменен', '2'
    '21', 'Ордер переведен в успех', '2'
    '22', 'Недостаточно средств', '2' 20
    '23', 'Нет возможности соверщить перевод', '2' 20
    '24', 'Реквизиты заблокированы', '2' 20
    '25', 'Реквизиты разблокированы', '2'
    '29', 'Не верно указаные реквизиты'
    '30', 'Не возможно совершить платеж на указанные реквизиты'
    '26', 'Реквизиты отключены, если нет доступа к автоматике', '3'
    '27', 'Автоматизация через телеграм отключена', '3'
    '28', 'Ордер удален', '3'

    :return:
    """
    pass
    # with cpy.connect(**config.config) as cnx:
    #     with cnx.cursor(dictionary=True) as cur:
    #         string0 = "SELECT * FROM pay_orders"
    #         cur.execute(string0)
    #         data = cur.fetchall()
    #         if data:
    #             print(data)


def del_order_status_0_payin(time=-15):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM pay_orders where pay_notify_order_types_id = 0 and pay_id = 1 and " \
                      "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string0)
            data0 = cur.fetchall()
            if data0:
                for i in data0:
                    order_uuid = i.get('uuid')
                    string = "DELETE from pay_orders where " \
                             "uuid = '" + str(order_uuid) + "' and date_expiry < DATE_ADD(UTC_TIMESTAMP(), INTERVAL +24 hour)"
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        message = "PAYIN ордер " + str(
                            order_uuid) + "\n удален. не оплачен. " + "\n" + \
                                  "Время (utc): " + str(datetime.datetime.utcnow())
                        botgreenavipay.send_message(config.pay_main_group, message)
                        print("PAYIN Ордер отменен. Закончилось Время (utc) подтверждения оплаты", datetime.datetime.now())


def set_order_status_1_payin(time=-15):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM pay_orders where pay_notify_order_types_id = 1 and pay_id = 1 and " \
                         "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string0)
            data0 = cur.fetchall()
            if data0:
                for i in data0:
                    order_uuid = i.get('uuid')
                    string = "UPDATE pay_orders SET pay_notify_order_types_id = 9, date_expiry = DATE_ADD(UTC_TIMESTAMP(), INTERVAL +15 minute) where " \
                             "uuid = '" + str(order_uuid) + "'"
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        message = "PAYIN ордер " + str(
                            order_uuid) + "\n отменен. Закончилось Время (utc) подтверждения оплаты " + "\n" + \
                                  "Время (utc): " + str(datetime.datetime.utcnow())
                        botgreenavipay.send_message(config.pay_main_group, message)
                        print("PAYIN Ордер отменен. Закончилось Время (utc) подтверждения оплаты", datetime.datetime.now())


def set_order_status_8_payin(time=-15):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM pay_orders where pay_notify_order_types_id = 8 and pay_id = 1 and " \
                     "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string0)
            data0 = cur.fetchall()
            if data0:
                for i in data0:
                    order_uuid = i.get('uuid')
                    string = "UPDATE pay_orders SET pay_notify_order_types_id = 5 where " \
                             "uuid = '" + str(order_uuid) + "'"
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        message = "PAYIN ордер "+str(order_uuid)+"\n переведен в диспут по истечения срока оплаты " + "\n" + \
                                  "Время (utc): " + str(datetime.datetime.utcnow())
                        botgreenavipay.send_message(config.pay_main_group, message)
                        print("PAYIN переведен в диспут по истечения срока оплаты", datetime.datetime.now())


def set_order_status_9_payin(time=-15):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 0 where " \
                     "pay_notify_order_types_id = 9 and pay_id = 1 and " \
                     "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                print("PAYIN переведены в статус Ордер отменен", datetime.datetime.now())



def set_order_status_15_payout(time=-240): #ПРИНЯТЬ
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 0 where " \
                     "pay_notify_order_types_id = 15 and pay_id = 2 and " \
                     "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                message = "PAYOUT Закончилось время подтверждения принятия " + "\n" + \
                          "Время (utc): " + str(datetime.datetime.utcnow())
                botgreenavipay.send_message(config.pay_main_group, message)
                print("PAYOUT Закончилось время подтверждения принятия", datetime.datetime.now())



def set_order_status_16_payout(time=-240): #ПОДТВЕРДИТЬ
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 17 where " \
                     "pay_notify_order_types_id = 16 and pay_id = 2 and " \
                     "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                message = "PAYOUT Закончилось время подтверждения оплаты " + "\n" + \
                          "Время (utc): " + str(datetime.datetime.utcnow())
                botgreenavipay.send_message(config.pay_main_group, message)
                print("PAYOUT Закончилось время подтверждения оплаты", datetime.datetime.now())



def set_order_status_17_payout(time=-240): #переведен в диспут
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 18 where " \
                     "pay_notify_order_types_id = 17 and pay_id = 2 and " \
                     "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                message = "PAYOUT Ордер переведен в диспут " + "\n" + \
                          "Время (utc): " + str(datetime.datetime.utcnow())
                botgreenavipay.send_message(config.pay_main_group, message)
                print("PAYOUT Ордер переведен в диспут")



def set_order_status_18_payout(time=-240):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 9 where " \
                     "pay_notify_order_types_id = 1 and pay_id = 2 and " \
                     "date_expiry < UTC_TIMESTAMP()"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                message = "PAYOUT переведены в статус Ордер отменен " + "\n" + \
                          "Время (utc): " + str(datetime.datetime.now(datetime.UTC))
                botgreenavipay.send_message(config.pay_main_group, message)
                print("PAYOUT переведены в статус Ордер отменен")


def get_payments():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_history where status = 'waiting' and type = 1"
            cur.execute(string)
            data = cur.fetchall()
            if data:
                for i in data:
                    print(i['payment_id'])
                    url = f"{config.base_url_np}payment/{i['payment_id']}"
                    headers = {
                        "x-api-key": config.api_key_np,
                        "Content-Type": "application/json"
                    }
                    response = requests.get(url, headers=headers)
                    print(response.json())
                    status = response.json()["payment_status"]
                    id = i['id']
                    #status = 'finished'
                    paid_amount = response.json()["actually_paid"]
                    try:
                        outcome_price = response.json()["outcome_amount"]
                    except:
                        outcome_price = 0
                    #value = i['value']
                    user_id = i['user_id']
                    if status == 'waiting':
                        print('В обработке')
                    if status == 'failed':
                        print('Ошибка')
                    if status == 'expired':
                        print('Просрочен')
                    #finished
                    if status == 'finished' and outcome_price > 0:
                        #пополнили депозит до лимит + остатки на баланс
                        print(user_id,":", outcome_price,":", status,":", id)
                        confirm_bal_or_dep_funds({'user_id': user_id, 'value': outcome_price, 'payment_status': status, 'id': id})

                    if status == 'partially_paid':
                        #на сумму actually_paid пополнили депозит до лимит + остатки на баланс
                        print(user_id, ":", paid_amount, ":", status, ":", id)
                        confirm_bal_or_dep_funds({'user_id': user_id, 'value': outcome_price, 'payment_status': status, 'id': id})

                    if status =='overpaid':
                        # на сумму actually_paid пополнили депозит до лимит + остатки на баланс
                        print(user_id, ":", paid_amount, ":", status, ":", id)
                        confirm_bal_or_dep_funds({'user_id': user_id, 'value': outcome_price, 'payment_status': status, 'id': id})

            else:
                print("нет входящих заявок на пополнение")


def get_payouts():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_history where status = 'CREATING' and type = 2"
            cur.execute(string)
            data = cur.fetchall()
            # creating;
            # processing;
            # sending;
            # finished;
            # failed;
            # rejected;
            if data:
                for i in data:
                    print(i['payment_id'])
                    url = f"{config.base_url_np}payout/{i['payment_id']}"
                    headers = {
                        "x-api-key": config.api_key_np,
                        "Content-Type": "application/json"
                    }
                    response = requests.get(url, headers=headers)
                    print(response.json())
                    status = response.json()['withdrawals'][0]["status"]
                    id = i['id']
                    #status = 'finished'
                    try:
                        paid_amount = response.json()['withdrawals'][0]["amount"]
                        #fee = response.json()["fee"]
                    except:
                        paid_amount = 0
                        #fee = 0
                    #value = paid_amount - fee
                    user_id = i['user_id']
                    if status == 'PROCESSING':
                        confirm_withdrawals_funds({'user_id': user_id, 'payment_status': status, 'id': id, 'value': paid_amount})
                        print('В обработке')
                    if status == 'SENDING':
                        confirm_withdrawals_funds({'user_id': user_id, 'payment_status': status, 'id': id, 'value': paid_amount})
                        print('отправляется')
                    if status == 'REJECTED':
                        confirm_withdrawals_funds({'user_id': user_id, 'payment_status': status, 'id': id, 'value': paid_amount})

                        print('Отказано')
                    #finished
                    if status == 'FINISHED':
                        #отправили на адрес value - fee
                        confirm_withdrawals_funds({'user_id': user_id, 'payment_status': status, 'id': id, 'value': paid_amount})
            else:
                print("нет исходящих заявок на вывод")


def confirm_withdrawals_funds(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            user_id = payload.get('user_id')
            status = payload.get('payment_status')
            withdrawals = float(payload.get('value'))
            id = payload.get('id')
            if status == 'FINISHED':
                select_string = "SELECT value from pay_balance where user_id = " + str(user_id)
                cur.execute(select_string)
                data0 = cur.fetchone()
                if data0:
                    value = float(data0.get('value'))
                    update_balance = "UPDATE pay_balance set withdrawals = 0, value = '" + str(
                    value - withdrawals) + "' where user_id = " + str(user_id)
                    cur.execute(update_balance)
                    cnx.commit()
                    status_string = "UPDATE pay_history SET status = '"+str(status)+"' where id = " + str(id)
                    cur.execute(status_string)
                    cnx.commit()
                else:
                    status_string = "UPDATE pay_history SET status = 'REJECTED' where id = " + str(id)
                    cur.execute(status_string)
                    cnx.commit()
            if status == 'REJECTED':
                select_string = "SELECT value, withdrawals from pay_balance where user_id = " + str(user_id)
                cur.execute(select_string)
                data0 = cur.fetchone()
                if data0:
                    value = float(data0.get('value'))
                    withdrawals = float(data0.get('value'))
                    update_balance = "UPDATE pay_balance set withdrawals = 0, value = '" + str(
                        value + withdrawals) + "' where user_id = " + str(user_id)
                    cur.execute(update_balance)
                    cnx.commit()
                    status_string = "UPDATE pay_history SET status = 'REJECTED' where id = " + str(id)
                    cur.execute(status_string)
                    cnx.commit()
                else:
                    status_string = "UPDATE pay_history SET status = 'REJECTED' where id = " + str(id)
                    cur.execute(status_string)
                    cnx.commit()









def confirm_bal_or_dep_funds(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            user_id = payload.get('user_id')
            value = payload.get('value')
            status = payload.get('payment_status')
            id = payload.get('id')
            check_balance = "SELECT * from pay_balance where baldep_status_id = 1" \
                            " and baldep_types_id = 1 and " \
                            "user_id = " + str(user_id)
            cur.execute(check_balance)
            data_bal = cur.fetchone()
            if data_bal:
                result_string = "UPDATE pay_balance SET value = " + str(data_bal.get('value') + value) + "where user_id = " + str(user_id)
                cur.execute(result_string)
                cnx.commit()
                if cur.rowcount > 0:
                    status_string = "UPDATE pay_history SET status = '"+str(status)+"' where id = " + str(id)
                    cur.execute(status_string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        print("Баланс пополнен, статус обновлен")
                    else:
                        print("Баланс пополнен, статус не обновлен")
                else:
                    print("Баланс пользователя", str(user_id), "не пополнен")
            else:
                print("Баланс пользователя", str(user_id), "не найден")


# generate_orders()
del_order_status_0_payin()
#set_order_status_1_payin()
set_order_status_8_payin()
set_order_status_9_payin()
set_order_status_15_payout()
get_payments()
get_payouts()

