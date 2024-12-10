import random
import uuid


import mysql.connector as cpy
import config


#check_orders
def check_orders():
    """
    (/set-order-status)
    '1', 'Получен ордер', '1' /create-order +
    '2', 'Ордер отменен', '1' /order-cancel
    '3', 'Ордер переведен в успех', '1' manual /order-success
    '4', 'Ордер оплачен клиентом', '1' manual /order-payed
    '5', 'Ордер переведен в диспут', '1' manual /order-disput
    '6', 'Ордер создан менеджером и переведен в диспут', '1' /order-manager-created
    '7', 'Успешный ордер переведен в отмену', '1' manual /order-cancel-confirmed из 3 в 2
    '8', 'Ордер переведен в диспут. Закончилось время подтверждения оплаты', '1' 4 -15 минут AUTO из 4
    '9', 'Ордер отменен. Закончилось время подтверждения оплаты', '1' 4 -15 минут AUTO из 1
    '10', 'Ордер подтвержден автоматикой', '1' /order-auto-confirmed
    '11', 'Ордер переведен из диспута в успех', '1' manual 8 -> 3 /order-confirmed
    '12', 'Ордер переведен из диспута в отмену', '1' manual 8 -> 2 /order-canceled
    '13', 'Реквизиты заблокированы', '1' manual /order-block-reqs
    '14', 'Реквизиты разблокированы', '1' manual /order-unblock-reqs

    '15', 'Получен ордер', '2'
    '16', 'Закончилось время подтверждения принятия', '2'
    '17', 'Закончилось время подтверждения оплаты', '2'
    '18', 'Ордер переведен в диспут', '2'
    '19', 'Ордер создан менеджером и переведен в диспут', '2'
    '20', 'Ордер отменен', '2'
    '21', 'Ордер переведен в успех', '2'
    '22', 'Реквизиты заблокированы', '2'
    '23', 'Реквизиты разблокированы', '2'

    '24', 'Реквизиты отключены, если нет доступа к автоматике', '3'
    '25', 'Автоматизация через телеграм отключена', '3'
    '26', 'Ордер удален', '3'
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


def get_orders_status_cancel_by_time_status_8(time=-15):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 8 where " \
                     "pay_notify_order_types_id = 4 and " \
                     "date < DATE_ADD(NOW(), INTERVAL "+str(time)+" minute)"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                print("переведен в диспут по истечения срока оплаты")
            else:
                print("никаких действий не проведено")


def get_orders_status_cancel_by_time_status_9(time=-15):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE pay_orders SET pay_notify_order_types_id = 9 where " \
                     "pay_notify_order_types_id = 1 and " \
                     "date < DATE_ADD(NOW(), INTERVAL "+str(time)+" minute)"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                print("переведены в статус Ордер отменен")
            else:
                print("никаких действий не проведено")


def generate_orders():
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            uuids = uuid.uuid4()
            data_string = "INSERT INTO pay_orders (uuid, user_id, course, chart_id, sum_fiat, pay_id," \
                  "value, cashback, date, date_expiry, req_id, pay_notify_order_types_id, docs_id) " \
                  "VALUES ('" + str(uuids) + "', 638,'" + str(random.randint(97,105)) + "',259,'" + \
                  str(random.randint(97,105)*100) + "',1,'" + str(random.randint(97,105)*100) + "','" \
                  + str(random.randint(1,10)) + "',NOW(), DATE_ADD(NOW(), INTERVAL 15 minute), 0, 1, 1)"
            print(data_string)
            cur.execute(data_string)
            cnx.commit()


#generate_orders()
get_orders_status_cancel_by_time_status_8()
get_orders_status_cancel_by_time_status_9()
#check_orders()
