from pydantic import BaseModel, HttpUrl
from hashlib import sha256
import mysql
from mysql.connector import errorcode
import logging
import time
import mysql.connector as cpy



class Logout(BaseModel):
    token: str


class RegisterRequest(BaseModel):
    login: str
    email: str
    telegram: str
    affiliate: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Code(BaseModel):
    email: str
    password: str
    code: str


class JwtRequest(BaseModel):
    email: str
    password: str


def insert_new_user(**payload):
    config = {
        'user': 'greenavi_user',
        'password': 'tb7x3Er5PQ',
        'host': '127.0.0.1',
        'database': 'greenavi_app',
        'raise_on_warnings': True
    }
    with cpy.connect(**config) as cnx:
        with cnx.cursor() as cur:
            app_id = 3
            comment = 'https://test.greenavi.com/confirm-register?login=' + str(payload['login'])
            data_login = "SELECT * from user where login = '" + str(payload['login']) + "' or email = '" + payload['email'] + "'"
            print(data_login)
            cur.execute(data_login)
            data = cur.fetchall()
            print(data)
            if not data:
                data_string = "INSERT INTO user (login, email, password, comment, telegram, app_id) " \
                              "VALUES ('" + str(payload['login']) + "','" + str(payload['email']) + \
                              "','" + str(payload['password']) + "','" + str(comment) + "','" + str(payload['telegram']) \
                              + "','" + str(app_id) + "')"
                cur.execute(data_string)
                cnx.commit()
                cnx.close()
                print(comment)
                return comment
            else:
                cnx.close()
                return "Пользователь уже существует"


class GetDbConnection():
    pass
