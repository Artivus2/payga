import mysql.connector as cpy
import config
from fastapi import HTTPException
import requests

async def get_all_stat_payin(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # общий оборот
            # if user_id == 0:
            #     dop_string = "user_id > 0"
            # else:
            dop_string = "user_id = " + str(user_id)
            string1 = "SELECT count(*) as all_orders, SUM(value) as all_orders_sum " \
                      "FROM pay_orders where pay_id = 1 and " + dop_string
            cur.execute(string1)
            data1 = cur.fetchone()
            p1 = 1
            p2 = 0
            if data1:
                p1 = data1.get('all_orders')
                p2 = data1.get('all_orders_sum')
            string2 = "SELECT count(*) as all_orders_success, SUM(value) as all_orders_sum_success, " \
                      "SUM(value * cashback / 100) as cashbk FROM pay_orders " \
                      "where pay_notify_order_types_id in (3, 11) and pay_id = 1 and " + dop_string
            cur.execute(string2)
            data2 = cur.fetchone()
            if data2:
                p3 = data2.get('all_orders_success')
                p4 = data2.get('all_orders_sum_success')
                p5 = data2.get('cashbk')
            else:
                p3=p4=p5=0

            string3 = "SELECT count(*) as all_orders_others, SUM(value) as all_orders_sum_others " \
                      "FROM pay_orders where pay_notify_order_types_id not in (3, 11) and pay_id = 1 and " + dop_string
            cur.execute(string3)
            data3 = cur.fetchone()
            if data3:
                p6 = data3.get('all_orders_others')
                p7 = data3.get('all_orders_sum_others')
            string4 = "SELECT AVG(value * cashback / 100) as average_check " \
                      "FROM pay_orders where pay_notify_order_types_id in (3, 11) and pay_id = 1 and " + dop_string
            cur.execute(string4)
            data4 = cur.fetchone()
            p8 = 0
            if data4:
                p8 = data4.get('average_check',0)
            if p8 is None:
                p8 = 0
            if p1 is None:
                p1 = 1
            try:
                conv = round(float(p3 / p1 * 100), 2)
            except:
                conv = 0

            data = {
                "all_orders": p1,
                "all_orders_sum": p2,
                "all_orders_success": p3,
                "all_orders_sum_success": p4,
                "cashbk": p5,
                "all_orders_others": p6,
                "all_orders_sum_others": p7,
                "conversion": conv,
                "average_check": round(float(p8),2)
            }
            return {"Success": True, "data": data}


async def get_all_stat_payout(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            # общий оборот
            # if user_id == 0:
            #     dop_string = "user_id > 0"
            # else:
            dop_string = "user_id = " + str(user_id)
            string1 = "SELECT count(*) as all_orders, SUM(value) as all_orders_sum " \
                      "FROM pay_orders where pay_id = 2 and " + dop_string
            cur.execute(string1)
            data1 = cur.fetchone()
            p1 = 1
            p2 = 0
            if data1:
                p1 = data1.get('all_orders')
                p2 = data1.get('all_orders_sum')
            string2 = "SELECT count(*) as all_orders_success, SUM(value) as all_orders_sum_success, " \
                      "SUM(value * cashback / 100) as cashbk FROM pay_orders " \
                      "where pay_notify_order_types_id = 21 and pay_id = 2 and " + dop_string
            cur.execute(string2)
            data2 = cur.fetchone()
            if data2:
                p3 = data2.get('all_orders_success')
                p4 = data2.get('all_orders_sum_success')
                p5 = data2.get('cashbk')
            else:
                p3=p4=p5=0

            string3 = "SELECT count(*) as all_orders_others, SUM(value) as all_orders_sum_others " \
                      "FROM pay_orders where pay_notify_order_types_id <> 21 and pay_id = 2 and " + dop_string
            cur.execute(string3)
            data3 = cur.fetchone()
            if data3:
                p6 = data3.get('all_orders_others')
                p7 = data3.get('all_orders_sum_others')
            string4 = "SELECT AVG(value * cashback / 100) as average_check " \
                      "FROM pay_orders where pay_notify_order_types_id = 21 and pay_id = 2 and " + dop_string
            cur.execute(string4)
            data4 = cur.fetchone()
            p8 = 0
            if data4:
                p8 = data4.get('average_check',0)
            if p8 is None:
                p8 = 0
            if p1 is None:
                p1 = 1
            try:
                conv = round(float(p3 / p1 * 100), 2)
            except:
                conv = 0

            data = {
                "all_orders": p1,
                "all_orders_sum": p2,
                "all_orders_success": p3,
                "all_orders_sum_success": p4,
                "cashbk": p5,
                "all_orders_others": p6,
                "all_orders_sum_others": p7,
                "conversion": conv,
                "average_check": round(float(p8),2)
            }
            return {"Success": True, "data": data}


async def get_stat_by_day_payin(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_all = "SELECT count(uuid) as count_orders, day(date) as day_filter, " + \
                       "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                       "where pay_id = 1 " + \
                       "and user_id = " +str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_sum = "SELECT sum(value) as sum, day(date) as day_filter, " + \
                         "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                         "where pay_id = 1 " + \
                         "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_all_success = "SELECT count(uuid) as count_orders, day(date) as day_filter, " + \
                         "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                         "where pay_notify_order_types_id in (3, 11) and pay_id = 1 " + \
                         "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_sum_success = "SELECT sum(value) as sum, day(date) as day_filter, " + \
                         "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                         "where pay_id = 1 " + \
                         "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_average = "SELECT SUM(value * cashback / 100) as cashbk, day(date) as day_filter, " + \
                                 "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                                 "where pay_id = 1 " + \
                                 "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            cur.execute(string_all)
            data0 = cur.fetchall()
            cur.execute(string_sum)
            data1 = cur.fetchall()
            cur.execute(string_all_success)
            data2 = cur.fetchall()
            cur.execute(string_sum_success)
            data3 = cur.fetchall()
            cur.execute(string_average)
            data4 = cur.fetchall()

            if data0 or data1 or data2 or data3 or data4:
                data = {
                    "all_orders_success": data0,
                    "all_orders_sum_success": data1,
                    "cashbk": data2,
                    "conversion": data3,
                    "average_check": data4
                }
                return {"Success": True, "data": data}
            else:
                data = {
                    "all_orders_success": [],
                    "all_orders_sum_success": [],
                    "cashbk": [],
                    "conversion": [],
                    "average_check": []
                }
                return {"Success": True, "data": data}


async def get_stat_by_day_payout(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_all = "SELECT count(uuid) as count_orders, day(date) as day_filter, " + \
                       "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                       "where pay_id = 2 " + \
                       "and user_id = " +str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_sum = "SELECT sum(value) as sum, day(date) as day_filter, " + \
                         "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                         "where pay_id = 2 " + \
                         "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_all_success = "SELECT count(uuid) as count_orders, day(date) as day_filter, " + \
                         "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                         "where pay_notify_order_types_id = 21 and pay_id = 2 " + \
                         "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_sum_success = "SELECT sum(value) as sum, day(date) as day_filter, " + \
                         "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                         "where pay_id = 2 " + \
                         "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            string_average = "SELECT SUM(value * cashback / 100) as cashbk, day(date) as day_filter, " + \
                                 "month(date) as month_filter, year(date) as year_filter FROM pay_orders " + \
                                 "where pay_id = 2 " + \
                                 "and user_id = " + str(payload.user_id) + " group by  day(date), month(date), year(date)"
            cur.execute(string_all)
            data0 = cur.fetchall()
            cur.execute(string_sum)
            data1 = cur.fetchall()
            cur.execute(string_all_success)
            data2 = cur.fetchall()
            cur.execute(string_sum_success)
            data3 = cur.fetchall()
            cur.execute(string_average)
            data4 = cur.fetchall()

            if data0 or data1 or data2 or data3 or data4:
                data = {
                    "all_orders_success": data0,
                    "all_orders_sum_success": data1,
                    "cashbk": data2,
                    "conversion": data3,
                    "average_check": data4
                }
                return {"Success": True, "data": data}
            else:
                data = {
                    "all_orders_success": [],
                    "all_orders_sum_success": [],
                    "cashbk": [],
                    "conversion": [],
                    "average_check": []
                }
                return {"Success": True, "data": data}


