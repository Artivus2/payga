import mysql.connector as cpy
import config


async def create_order_for_user(**payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_string = "INSERT INTO orders (uuid, user_id, course, chart_id, sum_fiat, pay_id," \
                          "value, cashback, date, date_expiry, req_id, pay_notify_order_types_id, docs_id " \
                          "VALUES ('" + str(payload['uuid']) + "','" + str(payload['user_id']) + \
                          "','" + str(payload['course']) + "','" + str(payload['chart_id']) + "','" + \
                          str(payload['sum_fiat']) + "','" + str(payload['value']) + "','" \
                          + str(payload['cashback']) + "','" + str(payload['date']) + "','" \
                          + str(payload['date_expiry']) + "','" + str(payload['req_id']) + "','" \
                          + str(payload['pay_notify_order_types_id']) + "','" + str(payload['docs_id']) + "')"
            cur.execute(data_string)
            cnx.commit()

            data_check = "select id from orders where uuid = " + str(payload['uuid'])
            cur.execute(data_check)
            check = cur.fetchone()
            if check:
                return {"Success": True, "data": "Ордер поставлен в очередь. Ожидайте исполнения"}
            else:
                return {"Success": False, "data": "Ордер не может быть создан"}


async def get_orders_by_any(payload):
    """
    фильтр по указанным параметрам
    :param payload:
    :return:
    """
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            null_id = payload.get('id', 0)
            data_check = "select pay_orders.id, pay_orders.user_id, course, pay_orders.chart_id, " \
                         "chart.symbol as chart_symbol, sum_fiat, pay_pay.id as pay_id, " \
                         "pay_pay.title as pay_id_title, pay_orders.value, cashback, " \
                         "pay_orders.date, date_expiry, pay_reqs.uuid as pay_reqs_uuid, " \
                         "pay_notify_order_types_id, pay_notify_order_types.title as " \
                         "pay_notify_order_types_title, pay_docs.url as pay_docs_url from pay_orders " \
                         "LEFT JOIN chart ON pay_orders.chart_id = chart.id " \
                         "LEFT JOIN pay_pay ON pay_orders.pay_id = pay_pay.id " \
                         "LEFT JOIN pay_reqs ON pay_orders.req_id = pay_reqs.id " \
                         "LEFT JOIN pay_docs ON pay_orders.docs_id = pay_docs.order_id " \
                         "LEFT JOIN pay_notify_order_types ON pay_orders.pay_notify_order_types_id = " \
                         "pay_notify_order_types.id " \
                         "where "
            if int(null_id) == 0:
                data_check += "pay_orders.id > 0"
            else:
                for k, v in dict(payload).items():
                    data_check += "pay_orders." + str(k) + " = '" + str(v) + "' and "
                data_check += "pay_orders.id is not null"

            print(data_check)

            cur.execute(data_check)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Ордер не найден"}


async def update_order_by_id(order_id, status):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # def check_status
            try:
                string = "UPDATE orders set pay_notify_order_types_id = '" + str(status) + \
                         "where id = " + str(order_id)
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Статус успешно изменен"}
            except:
                return {"Success": True, "data": "Статус не может быть изменен"}


async def delete_order_by_id(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # def check_status_for_delete статус удален ???
            try:
                string = "UPDATE orders set pay_notify_order_types_id = 0 where id = " + str(id)
                cur.execute(string)
                cnx.commit()
                return {"Success": True, "data": "Успешно изменен"}
            except:
                return {"Success": True, "data": "Статус не может быть изменен"}


async def insert_docs(order_id, images):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            try:
                for i in images:
                    data_string = "INSERT into docs (order_id, url) " \
                                  "VALUES ('" + str(order_id) + "','" + str(i) + "')"
                    cur.execute(data_string)
                    cnx.commit()
                cnx.close()
                return {"Success": True, "data": "Документы добавлены"}
            except:
                return {"Success": False, "data": "Платежки не добавлены"}


async def get_docs_urls(order_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select * from pay_docs where order_id = " + str(order_id)
            cur.execute(data_check)
            check = cur.fetchall()
            if check:
                return {"Success": True, "data": check}
            else:
                return {"Success": False, "data": "Платежки не найдены"}
