import mysql.connector as cpy
import config
from routers.user.utils import create_random_key


async def insert_new_user_banned(**payload):
    # try todo
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            app_id = 3  # paygreenavi
            link_gen = await create_random_key()
            data_login = "SELECT * from user where login = '" + str(payload['login']) + \
                         "' or email = '" + payload['email'] + "'"
            cur.execute(data_login)
            data = cur.fetchall()
            data_ref = "SELECT id from user where id = '" + str(payload['affiliate_invitation_id']) + "'"
            cur.execute(data_ref)
            ref_id = cur.fetchone()[0]
            if not ref_id:
                ref_id = 0
            if not data:
                banned_for_submit = 1 # блокируем вход до подтверждения админом
                data_string = "INSERT INTO user (login, email, password, affiliate_invitation_id, comment, telegram, app_id, banned) " \
                              "VALUES ('" + str(payload['login']) + "','" + str(payload['email']) + \
                              "','" + str(payload['password']) + "','" + str(ref_id) + "','" + str(
                    link_gen) + "','" + str(payload['telegram']) + "','" + str(app_id) + "','" + str(banned_for_submit) + "')"

                cur.execute(data_string)
                cnx.commit()
                cnx.close()
                # print(comment)
                return {"status": True, "message": "Успешная регистрация"}
            else:
                return {"status": False, "message": "Пользователь: " + str(payload['email'])
                                                    + ' / ' + str(payload['login']) + " уже существует"}


async def send_link_to_user(id, login=None):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            string = "SELECT comment from user where id = '" + str(id) + \
                     "' or login = '" + str(login) + "'"
            cur.execute(string)
            data = cur.fetchone()
            if data:
                link = config.REG_URL + "/" + data[0]
                return {"link": link}
            cur.close()
