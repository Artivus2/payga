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



async def insert_generated_api_key(user_id):

    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            api_key = await create_random_key(45)
            string = "SELECT * from user where app_id = 3 and id = " + str(user_id)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                data_str = "INSERT INTO pay_api_keys (user_id, api_key, api_key_begin_date, api_key_expired_date, " \
                           "status) " \
                "VALUES ('" + str(user_id) + "','" + str(api_key) + "', NOW(),NOW() + interval " + str(config.API_KEY_EXPIRATION_PERIOD)+", 1)"
                print(data_str)
                cur.execute(data_str)
                cnx.commit()
                cnx.close()
                return {"Success": True, "api_key": api_key}
            else:
                return {"Success": False, "api_key": 'не создан'}

async def get_token_by_user_id(token):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            string = "SELECT token, expired_at from auth_tokens where expired_at > UNIX_TIMESTAMP() - 86400 and token = " \
                     "'" + str(token) + "'"
            print(string)
            cur.execute(string)
            data = cur.fetchone()

            print(data)
            if data:
                return {"Status": True, "token":data[0]}
            else:
                return {"Status": False, "token": "Токен не найден или просрочен"}
