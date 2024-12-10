from datetime import datetime

import mysql.connector as cpy


import config
import routers.admin.models as admin_models
from routers.user.controller import create_random_key
import telebot
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
                              "affiliate_invitation_code, telegram, app_id, banned) " \
                              "VALUES ('" + str(payload['login']) + "','" + str(payload['email']) + \
                              "','" + str(payload['password']) + "','" + str(ref_id) + "','" + str(
                    link_gen) + "','" + str(payload['telegram']) + "','" + str(app_id) + "','" + str(
                    banned_for_submit) + "')"
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
                message = "Пользователь " + str(payload['email'])\
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


async def crud_roles(crud, payload): # todo -> admin
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
                string = "UPDATE pay_admin_roles set title = '" +str(payload.title) + \
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
                string = "UPDATE pay_admin_roles set status = '"+str(payload.status) \
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


async def set_users_any(payload): # эталон для update
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
