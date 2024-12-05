import mysql.connector as cpy
import config


async def get_all_stat(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # общий оборот
            string1 = "SELECT count(*) as all_orders, SUM(value) as all_orders_sum " \
                      "FROM pay_orders where " \
                      "user_id = " + str(user_id)
            cur.execute(string1)
            data1 = cur.fetchone()
            string2 = "SELECT count(*) as all_orders_success, SUM(value) as all_orders_sum_success, " \
                      "SUM(value * cashback / 100) as cashbk FROM pay_orders " \
                      "where pay_notify_order_types_id in (3, 11) and " \
                      "user_id = " + str(user_id)
            cur.execute(string2)
            data2 = cur.fetchone()

            string3 = "SELECT count(*) as all_orders_others, SUM(value) as all_orders_sum_others " \
                      "FROM pay_orders where pay_notify_order_types_id not in (3, 11) and " \
                      "user_id = " + str(user_id)
            cur.execute(string3)
            data3 = cur.fetchone()
            string4 = "SELECT AVG(value * cashback / 100) as average_check " \
                      "FROM pay_orders where pay_notify_order_types_id in (3, 11) and " \
                      "user_id = " + str(user_id)
            cur.execute(string4)
            data4 = cur.fetchone()
            data = {
                "all_orders": data1.get('all_orders', 0),
                "all_orders_sum": data1.get('all_orders_sum', 0),
                "all_orders_success": data2.get('all_orders_success', 0),
                "all_orders_sum_success": data2.get('all_orders_sum_success', 0),
                "cashbk": data2.get('cashbk', 0),
                "all_orders_others": data3.get('all_orders_others',0),
                "all_orders_sum_others": data3.get('all_orders_sum_others', 0),
                "conversion": float((data2.get('all_orders_success', 0) /
                                     data1.get('all_orders', 1) * 100).__format__('2.2f')),
                "average_check": float(data4.get('average_check', 0).__format__('2.2f'))
            }
            return {"Success": True, "data": data}

