import json
import routers.mains.models as mains_models
import requests
from fastapi import APIRouter, HTTPException
from routers.mains.controller import (
    get_bank,
    get_chart,
    get_reqs_by_user,
    get_reqs_groups_by_id,
    req_by_filters
)

router = APIRouter(prefix='/api/v1/mains', tags=['Mains'])

@router.get("/get-banks/{id}")
async def get_bank_by_id(id: str):
    """
    Запрос банка
    :param token:
    :return:
    token
    """
    response = await get_bank(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    print(response)
    return response


@router.get("/get-chart/{id}")
async def get_chart_by_id(id: str):
    """
    Запрос крипты
    :param chart:
    :return:

    """
    response = await get_chart(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    print(response)
    return response


@router.post("/get-reqs")
async def get_reqs_by_user(user_id: int):
    """
    Запрос реквизитов пользователя по user_id
    :param dict:
    :return:

    """
    response = await get_reqs_by_user(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    print(response)
    return response


@router.post("/get-reqs-filter")
async def filter_reqs(request: mains_models.Reqs):
    """
    Запрос реквизитов пользователя по параметрам
    :param request:
    :param dict:
    :return:

    """
    payload = {}
    for k, v in request:
        print(k, v)
        if v is not None:
            payload[k] = v
    response = await req_by_filters(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.get("/get-reqs-groups/{id}")
async def get_reqs_groups(id: int):
    """
    Запрос реквизитов группы
    :param request:
    :param dict:
    :return:
    """
    response = await get_reqs_groups_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response.json()
        )
    print(response)
    return response