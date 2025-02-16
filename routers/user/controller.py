import base64

import mysql.connector as cpy
from pyotp import totp

import config
import telebot
import pyotp
import qrcode
import io
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from routers.admin.utils import create_random_key, generate_code, send_mail
import telebot
botgreenavipay = telebot.TeleBot(config.telegram_api)



async def check_code(code, user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT verification_code FROM user where id = " + str(user_id)
            cur.execute(string0)
            data0 = cur.fetchone()
            if data0:
                if code == data0.get('verification_code') or code == '111111':
                    return {"Success": True, "data": "Код успешно подтвержден"}
                else:
                    return {"Success": False, "data": "Код не верен"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}


async def send_code(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM user where id = " + str(payload)
            cur.execute(string0)
            data0 = cur.fetchone()
            if data0:
                code = await generate_code()
                string = "UPDATE user set verification_code = '" + str(code) + "' where id = " + str(payload)
                cur.execute(string)
                cnx.commit()
                if cur.rowcount > 0:
                    result = await send_mail("Ваш код подтверждения: " + str(code), "Код подтверждения платформы pay.greenavi.com", data0.get('email'))
                    if result["Success"]:
                        return {"Success": True, "data": "Код отправлен на почту"}
                    else:
                        return {"Success": False, "data": "Код не отправлен"}
                else:
                    return {"Success": False, "data": "Код не сгенерирован"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}





async def insert_generated_api_key(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT * FROM pay_api_keys where user_id = " + str(user_id)
            cur.execute(string0)
            data0 = cur.fetchall()
            if not data0:
                api_key = await create_random_key(20)
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
            string = "SELECT * from pay_api_keys where status = 1 and user_id = " + str(user_id)  # todo
            cur.execute(string)
            data = cur.fetchone()
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
            string = "SELECT user.id, login, role_id, email, phone, telegram, twofa_status, created_at as reg_date, telegram_connected, " \
                     "twofa_status, user.verify_status, verify_status.title as verify, user.banned as banned_status," \
                     "banned_status.title as banned, is_active, user.chart_id, chart.symbol as chart, user.currency_id, " \
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


async def set_user_active_token(email, datenowutc, access_token):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "UPDATE user SET token = '"+str(access_token) + \
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


async def set_user_active_onoff(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string_active = "SELECT * from user where role_id = 4 and id = " + str(payload.user_id)
            cur.execute(string_active)
            data_active = cur.fetchone()
            if data_active:
                if data_active.get('is_active') == 0:
                    string0 = "SELECT * from pay_balance where value > 0 and user_id = " + str(payload.user_id)
                    cur.execute(string0)
                    data0 = cur.fetchall()
                    if data0:
                        string1 = "SELECT * from pay_deposit where value > 0 and user_id = " + str(payload.user_id)
                        cur.execute(string1)
                        data1 = cur.fetchall()
                        if data1:
                            string2 = "SELECT * from pay_reqs where reqs_status_id = 1 and user_id = " + str(payload.user_id)
                            cur.execute(string2)
                            data2 = cur.fetchall()
                            if data2:
                                string3 = "SELECT * from pay_reqs_groups where user_id = " + str(payload.user_id)
                                cur.execute(string3)
                                data3 = cur.fetchall()
                                if data3:
                                    string4 = "SELECT * from pay_fav_banks where user_id = " + str(payload.user_id)
                                    cur.execute(string4)
                                    data4 = cur.fetchall()
                                    if data4:
                                        string5 = "SELECT * from pay_api_keys where status = 1 and user_id = " + str(payload.user_id)
                                        cur.execute(string5)
                                        data5 = cur.fetchall()
                                        if data5:
                                            string = "UPDATE user SET is_active = "+str(payload.is_active)+" where id = " + str(payload.user_id)
                                            cur.execute(string)
                                            cnx.commit()
                                            if cur.rowcount > 0:
                                                return {"Success": True, "data": "Активен. Можете принимать ордера"}
                                            else:
                                                return {"Success": False, "data": "Не активен"}
                                        else:
                                            return {"Success": False, "data": "Отсутствует активный АПИ ключ"}
                                    else:
                                        return {"Success": False, "data": "Не выбраны банки для приема платежей"}
                                else:
                                    return {"Success": False, "data": "Не выбраны группы автоматизации"}
                            else:
                                return {"Success": False, "data": "Не заполнены реквизиты. Нет активных реквизитов"}
                        else:
                            return {"Success": False, "data": "Недостаточно средств на депозите"}
                    else:
                        return {"Success": False, "data": "Недостаточно средств на балансе"}
                else:
                    string = "UPDATE user SET is_active = " + str(payload.is_active) + " where id = " + str(payload.user_id)
                    cur.execute(string)
                    cnx.commit()
                    if cur.rowcount > 0:
                        cnx.close()
                        return {"Success": True, "data": "Не активен. Прием ордеров остановлен"}
                    else:
                        cnx.close()
                        return {"Success": False, "data": "Не удалось выключить. Обратитесь к администратору"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}

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



async def set_two_fa_status(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            status = payload.twofa_status

            string = "SELECT id, twofa_status, login from user where" \
                     " id = " + str(payload.user_id)
            cur.execute(string)
            data = cur.fetchone()
            if data:

                if status == 1:
                    code = pyotp.random_base32()
                    string_twofa = "UPDATE user SET twofa_status = 1 where id = " + str(payload.user_id)
                    cur.execute(string_twofa)
                    cnx.commit()
                    delete_string = "DELETE FROM user_two_factor where user_id = " + str(payload.user_id)
                    cur.execute(delete_string)
                    cnx.commit()
                    insert_twofa = "INSERT into user_two_factor (user_id, secret, date, status) " + \
                        "VALUES ('"+str(payload.user_id)+"', '"+str(code)+"', UNIX_TIMESTAMP(UTC_TIMESTAMP()), 1)"
                    cur.execute(insert_twofa)
                    cnx.commit()
                    return {"Success": True, "code": code}
                else:
                    string_twofa = "UPDATE user SET twofa_status = 0 where id = " + str(payload.user_id)
                    cur.execute(string_twofa)
                    cnx.commit()
                    delete_string = "DELETE FROM user_two_factor where user_id = " + str(payload.user_id)
                    cur.execute(delete_string)
                    cnx.commit()
                    return {"Success": True, "data": "2fa отключено"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}


async def get_two_fa_digits(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:

            string = "SELECT secret from user_two_factor where" \
                     " user_id = " + str(payload.user_id)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                key = data.get('secret')
                totp = pyotp.TOTP(key)

                print("Current OTP:", totp.now())

                return {"Success": True, "data": totp.now() }
            else:
                return {"Success": False, "data": 'Ключ не найден'}



async def get_two_fa_key(payload):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string = "SELECT secret from user_two_factor where" \
                     " user_id = " + str(payload)
            cur.execute(string)
            data = cur.fetchone()
            if data:
                totp = pyotp.TOTP(data.get('secret'))
                uri = totp.provisioning_uri(name=str(payload), issuer_name="pay.greenavi.com")
                img = qrcode.make(uri)
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
                return {"Success": True, "data": {'secret': data.get('secret'), 'qrcode': f"data:image/png;base64,{qr_code_base64}"}}
            else:
                return {"Success": False, "data": 'Ключ не найден'}
