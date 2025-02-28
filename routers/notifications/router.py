
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
import requests
from starlette.requests import Request

import config
from routers.notifications import models
from routers.notifications.controller import (
    get_tg_messages_by_user_id,
    send_tg_messages_by_id
    )
# import telebot
# notify_bot = telebot.TeleBot(config.notification_bot_api)

router = APIRouter(prefix='/api/v1/notification',include_in_schema=False, tags=['Уведомления'])


# notify_bot.send_message('1168510917', 'test3')

# @notify_bot.message_handler(commands=["start"])
# def cmd_start(message):
#     """Инициализация диалога с ботом"""
#     # Создаем приветственный текст
#     welcome_text = f"Привет, {message.chat.first_name}!\n Сайт pay.greenavi.com привествует вас"
#     # Отправляем в чат
#     notify_bot.send_message(message.chat.id, welcome_text)
#     # Отправляем реплику в базу данных через API
#     #send_to_database(message.chat.id, welcome_text)
#     # Устанавливаем пользователю "состояние" первого вопроса
#     #set_user_state(message.chat.id, StatesOfTalk.FIRST_QUESTION.value)


@router.get("/get-notification/{user_id}")
async def get_tg_message(user_id: int):
    """
    Get notification info from telegram
    :return:
    """
    response = await get_tg_messages_by_user_id(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


# @router.get("/send-notification/{tg_id}")
# async def get_tg_message(request: models.Notification):
#     """
#     Get notification info from telegram
#
#     :return:
#     """
#     response = await get_tg_messages_by_user_id()
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response,
#         )
#     return response
