import json
import sqlite3

import routers.roles.models as roles_models
import requests
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix='/api/v1/operator', tags=['Оператор'])



@router.get("/get-api-status")
async def get_api_status():
    """
    https://pay.greenavi.com/api/v1/merchant/get-api-status
    Проверка статуса API
    :param request:
    :return:
    """

    return {"Success": True, "data": "API доступна"}