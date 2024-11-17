from pydantic import BaseModel
from hashlib import sha256
import mysql
from mysql.connector import errorcode
import logging
import time


class Login(BaseModel):
    email: str
    password: str


class SendCode(BaseModel):
    code: str


class JwtRequest(BaseModel):
    email: str
    password: str

    def get_db_connection(self):
        config = {
            'user': 'greenavi_user',
            'password': 'tb7x3Er5PQ',
            'host': '127.0.0.1',
            'database': 'greenavi_app',
            'raise_on_warnings': True
        }

        cnx = mysql.connector.connect(**config)
        try:
            cnx = mysql.connector.connect(config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()