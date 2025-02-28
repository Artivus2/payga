import mysql.connector as cpy
import config
import json
import telebot
notify_bot = telebot.TeleBot(config.notification_bot_api)




async def get_tg_messages_by_user_id(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            data_check = "select message, DATE_FORMAT(date, "+str(config.date_format_all)+") as date, status from pay_notification where user_id = " + str(user_id) + " order by id desc"
            cur.execute(data_check)
            print(data_check)
            data = cur.fetchall()
            if data:
                return {"Success": True, "data": data}
            else:
                return {"Success": False, "data": "Сообщения не найдены"}



async def send_tg_messages_by_id(user_id, text):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor(dictionary=True) as cur:
            string0 = "SELECT id, telegram_connected, telegram FROM user where id = " + str(user_id)
            cur.execute(string0)
            data0 = cur.fetchone()
            print(data0)
            print(user_id, text)
            if data0:
                user_id = data0.get('id')
                telegram_connected = data0.get('telegram_connected')
                if telegram_connected > 0 and user_id > 0:

                    status = "Отправлено"
                    try:
                        notify_bot.send_message(telegram_connected, text)
                        print("Уведомление отправлено")
                    except:
                        print("Не удалось отправить уведомление")
                        status = "Не удалось отправить"
                    insert_string = "INSERT INTO pay_notification (user_id, message, date, status) " \
                                    "VALUES ('" + str(user_id) + "','" + str(text) + \
                                    "', UTC_TIMESTAMP(), '"+str(status)+"')"
                    cur.execute(insert_string)
                    cnx.commit()
                    if cur.rowcount > 0:

                        return {"Success": True, "data": "Уведомление отправлено"}
                    else:
                        return {"Success": False, "data": "Сообщение не удалось отправить"}
                else:
                    return {"Success": False, "data": "Телеграм не подключен"}
            else:
                return {"Success": False, "data": "Пользователь не найден"}

