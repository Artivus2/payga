import datetime
import random
import uuid
import mysql.connector as cpy
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
                          "Время (utc): " + str(datetime.datetime.utcnow())
                botgreenavipay.send_message(config.pay_main_group, message)
                print("PAYOUT переведены в статус Ордер отменен")



# def set_order_status_222324_payout(time=-240):
#     with cpy.connect(**config.config) as cnx:
#         with cnx.cursor(dictionary=True) as cur:
#             string = "UPDATE pay_orders SET pay_notify_order_types_id = 20 where " \
#                      "pay_notify_order_types_id in (22,23,24) and pay_id = 2 and " \
#                      "date_expiry < UTC_TIMESTAMP()"
#             cur.execute(string)
#             cnx.commit()
#             if cur.rowcount > 0:
#                 print("PAYOUT переведены в статус Ордер отменен")
#             else:
#                 print("никаких действий не проведено")


# def generate_orders():
#     with cpy.connect(**config.config) as cnx:
#         with cnx.cursor(dictionary=True) as cur:
#             uuids = uuid.uuid4()
#             pay_id = 1 #payin
#             pay_notify_order_types_id = 0
#             req_id = 17
#             user_id=628
#             data_string = "INSERT INTO pay_orders (uuid, user_id, course, chart_id, sum_fiat, pay_id," \
#                           "value, cashback, date, date_expiry, req_id, pay_notify_order_types_id, docs_id) " \
#                           "VALUES ('" + str(uuids) + "', '"+str(user_id)+"','" + str(random.randint(97, 105)) + "',259,'" + \
#                           str(random.randint(97, 105) * 100) + "','"+str(pay_id)+"','" + str(random.randint(97, 105) * 100) + "','" \
#                           + str(random.randint(1, 10)) + "',UTC_TIMESTAMP(), DATE_ADD(UTC_TIMESTAMP(), INTERVAL 15 minute), '"+str(req_id)+"', '"+str(pay_notify_order_types_id)+"', 1)"
#             print(data_string)
#             cur.execute(data_string)
#             cnx.commit()
#

# generate_orders()
del_order_status_0_payin()
#set_order_status_1_payin()
set_order_status_8_payin()
set_order_status_9_payin()
set_order_status_15_payout()
# set_order_status_16_payout()
# set_order_status_17_payout()
# set_order_status_18_payout()
#set_order_status_222324_payout()

# check_orders()
#print("ok", datetime.datetime.now())


