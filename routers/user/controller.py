import mysql.connector as cpy
import config
from routers.user.utils import create_random_key


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


async def insert_generated_api_key(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            api_key = await create_random_key(45)
            string = "SELECT * from user where app_id = 3 and banned = 0 and id = " + str(user_id)
            cur.execute(string)
            data1 = cur.fetchone()
            if data1:
                string = "SELECT * from pay_api_keys where status = 1 and id = " + str(user_id)
                cur.execute(string)
                data2 = cur.fetchone()
                if not data2:
                    data_str = "INSERT INTO pay_api_keys (user_id, api_key, api_key_begin_date, api_key_expired_date, " \
                               "status) " \
                               "VALUES ('" + str(user_id) + "','" + str(api_key) + \
                               "', NOW(),NOW() + interval " + str(config.API_KEY_EXPIRATION_PERIOD) + ", 1)"
                    cur.execute(data_str)
                    cnx.commit()
                    cnx.close()
                    return {"Success": True, "data": api_key}
                else:
                    return {"Success": False, "data": 'не создан'}
            else:
                return {"Success": False,
                        "data": 'у вас есть действующий ключ, обратитесь к администратору для смены ключа'}


async def get_user_api_key(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_api_keys where status in (0,1,3) and user_id = " + str(user_id)  # todo
            cur.execute(string)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": 'не найден'}


async def delete_user_api_key_by_id(id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from pay_api_keys where id = " + str(id)
            cur.execute(string)
            data = cur.fetchall()
            if data:
                data_str = "UPDATE pay_api_keys SET status = 2 where id = " + str(id)
                cur.execute(data_str)
                cnx.commit()
                cnx.close()
                return {"Success": True, "data": "Успешно"}
            else:
                return {"Success": False, "data": 'не удален'}


async def get_token_by_token(token):
    print(token)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT user_id, token, expired_at from auth_tokens where " \
                     "expired_at > UNIX_TIMESTAMP() - 86400 and token = " \
                     "'" + str(token) + "'"
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data['user_id']}
            else:
                return {"Success": False, "data": "Токен не найден или просрочен"}


async def get_refresh_token(token):
    """

    :param token:
    :return:
    """


async def get_profile_by_id(user_id):
    """
    получаем все данные пользователя
    :param user_id:
    :return:
    """
    # todo dic(zip)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT user.id, login, email, telegram, created_at as reg_date, telegram_connected, " \
                     "twofa_status, user.verify_status, verify_status.title as verify, user.banned as banned_status," \
                     "banned_status.title as banned, user.chart_id, chart.symbol as chart, user.currency_id, " \
                     "currency.symbol as currency from user " \
                     "LEFT JOIN verify_status ON user.verify_status = verify_status.id " \
                     "LEFT JOIN banned_status ON user.banned = banned_status.id " \
                     "LEFT JOIN chart ON user.chart_id = chart.id " \
                     "LEFT JOIN currency ON user.currency_id = currency.id " \
                     "where user.id = " + str(user_id)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Токен не найден или просрочен"}


async def check_user_by_id(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT * from user where id = " + str(user_id)
            print(string)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Пользователь не найден"}
