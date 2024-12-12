import mysql.connector as cpy
import config
import telebot
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from routers.admin.utils import create_random_key
import telebot
botgreenavipay = telebot.TeleBot(config.telegram_api)

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
                if cur.rowcount > 0:
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


# async def get_refresh_token(token):
#     """
#
#     :param token:
#     :return:
#     """


async def get_profile_by_id(user_id):
    """
    получаем все данные пользователя
    :param user_id:
    :return:
    """
    # todo dic(zip)
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT user.id, login, role_id, email, phone, telegram, created_at as reg_date, telegram_connected, " \
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


async def get_user_by_email(email):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT id, login, email, password, role_id from user where" \
                     " banned = 0 and email = '" + str(email) + "'"
            cur.execute(string)
            data = cur.fetchone()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Пользователь не найден"}


async def set_user_active(email, datenowutc, access_token):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE user SET is_active = 1, token = '"+str(access_token) + \
                     "', last_visit_time = '"+str(datenowutc)+"' " \
                     "where email = '" + str(email) + "'"
            cur.execute(string)
            cnx.commit()
            if cur.rowcount > 0:
                cnx.close()
                message = "Пользователь " + str(email) + " авторизован в " + str(datetime.utcnow())
                botgreenavipay.send_message(config.pay_main_group, message)
                return {"Success": True, "data": "Успешно авторизован"}
            else:
                cnx.close()
                return {"Success": False, "data": "Ошибка авторизации"}


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(dbUtil.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
#         username = payload.get("subject")
#         expiration = datetime.strptime(payload.get("expiration"), "%Y-%m-%d %H:%M:%S")
#
#         if username is None:
#             raise credentials_exception
#
#         ## To check if the user have logged out or the token has expired
#         black_list = find_token_black_lists(token, db)
#         if black_list or (expiration <= datetime.now()):
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Token Experied! Please login again. ")
#
#     except (JWTError, ValidationError):
#         raise credentials_exception
#
#     # print("======================================",payload,"======================================",)
#
#     user = auth.find_existed_user(username, db);
#     if user is None:
#         raise credentials_exception
#     return user


# def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
#     if not bool(current_user.is_active):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


## ---------------------------- Auth CRUD Operations-------------------------------
## To create new token for a password reset
# def create_reset_code(request: schemas.EmailRequest, reset_code: str, db: Session):
#     query = f"""INSERT INTO codes(email,reset_code,status,expired_in)
#                 VALUES ('{request.email}','{reset_code}',1,'{(datetime.now() + timedelta(hours=8))}');"""
#
#     db.execute(query)
#     db.commit()
#
#     return {"Message": f"Reset Code created successfully for User with email {request.email}."}


## Replacing the old password with the new password for the given email
# def reset_password(new_password: str, email: str, db: Session):
#     query = f"""UPDATE users SET password='{cryptoUtil.get_hash(new_password)}' WHERE email='{email}';"""
#
#     db.execute(query)
#     db.commit()
#
#     return {"Message": f"Password reset successful for User with email {email}."}


## For diabling the reset token for the user after a successfull password reset
# def disable_reset_code(reset_password_token: str, email: str, db: Session):
#     query = f"""UPDATE codes
#                 SET status='0'
#                 WHERE
#                     status='1'
#                 AND
#                     reset_code='{reset_password_token}'
#                 OR
#                     email='{email}'
#                 ;"""
#     db.execute(query)
#     db.commit()
#
#     return {"Message": f"Reset code successfully disabled for User with email - {email}."}


## Finding if the user with the given email exsists or not
# def find_existed_user(email: str, db: Session):
#     user = db.query(models.User).filter(and_(models.User.email == email, models.User.is_active == True)).first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Either user with email {email} not found OR currently in-active !")
#     return user


## To check if the password reset token is valid or not
# def check_reset_password_token(token: str, db: Session):
#     query = f"""SELECT email FROM codes
#                 WHERE
#                     status='1'
#                 AND
#                     reset_code='{token}'
#                 AND
#                     expired_in >= CURRENT_TIMESTAMP
#                 ;"""
#
#     resultproxy = db.execute(query)
#
#     # The end result is the list which contains query results in tuple format
#     return [rowproxy for rowproxy in resultproxy]