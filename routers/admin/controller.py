import mysql.connector as cpy
import config
import routers.admin.models as admin_models
from routers.user.controller import create_random_key


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
        with cnx.cursor() as cur:
            # try todo
            data_string = "SELECT FROM user where id = '" + str(user_id) + "'"
            cur.execute(data_string)
            data = cur.fetchone()
            if data:
                string = "UPDATE user SET banned = 0 where id = '" + str(user_id) + "'"
                cur.execute(string)
                cnx.commit()
                return {"Success":True, "data": "Пользователь подтвержден"}
            cur.close()
    return {"Success":False, "data": "Пользователь подтвержден"}


async def insert_new_user_banned(**payload):
    # try todo
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            app_id = 3  # paygreenavi
            link_gen = await create_random_key()
            data_login = "SELECT id from user where login = '" + str(payload['login']) + \
                         "' or email = '" + payload['email'] + "'"
            cur.execute(data_login)
            data = cur.fetchone()
            data_ref = "SELECT id from user where comment = '" + str(payload['affiliate_invitation_code']) + "'"
            cur.execute(data_ref)
            ref_id = cur.fetchone()
            print("ref_id", ref_id)
            if ref_id:
                ref_id = ref_id['id']
            else:
                ref_id = 0
            if not data:
                banned_for_submit = 1  # блокируем вход до подтверждения админом
                data_string = "INSERT INTO user (login, email, password, affiliate_invitation_id, comment, telegram, app_id, banned) " \
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
                return {"Success": True, "data": "Поставлен в очередь на регистрацию. Ожидайте"}
            else:
                return {"Success": False, "data": "Пользователь: " + str(payload['email'])
                                                  + ' / ' + str(payload['login']) + " уже существует"}