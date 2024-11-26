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

router = APIRouter(prefix='/api/v1/mains', tags=['Основные'])

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


@router.put("/set-reqs")
async def set_reqs_by_user(user_id: int):
    """
    установка реквизитов пользователя по user_id
    :param dict:
    :return:
    """
    pass


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


@router.put("/set-reqs-groups")
async def set_reqs_groups(id: int):
    """
    Установка реквизитов группы
    :param request:
    :param dict:
    :return:
    """
    pass


@router.get("/get-pay-automation-history/{id}")
async def get_pay_automation_history(id: int):
    """
    Запрос типов автоматизации
    :param request:
    :param dict:
    :return:
    """
    pass


@router.get("/get-pay-automation-status/{id}")
async def get_pay_automation_status(id: int):
    """
    Запрос статусов автоматизации
    :param request:
    :param dict:
    :return:
    """
    pass


@router.get("/get-pay-reqs-status/{id}")
async def get_pay_reqs_status(id: int):
    """
    Запрос статусов реквизитов
    :param request:
    :param dict:
    :return:
    """
    pass


@router.get("/get-pay-reqs-types/{id}")
async def get_pay_reqs_types(id: int):
    """
    Запрос типов реквизитов
    :param request:
    :param dict:
    :return:
    """
    pass


@router.get("/get-pay-reqs-turn-off/{id}")
async def get_pay_automation_turn_off(id: int):
    """
    автоматическое выключение реквизитов без доступа к автоматике (1 - включено, 0 - выключено)
    :param request:
    :param dict:
    :return:
    """
    pass


@router.get("/get-pay-referal-types/{id}")
async def get_pay_refs_types(id: int):
    """
    Типы рефералов
    :param
    request:
    :param
    dict:
    :return:
    """
    pass


@router.get("/get-pay-referal/{user_id}")
async def get_pay_refs(id: int):
    """
    Рефералы по user_id
    :param
    request:
    :param
    dict:
    :return:
    """
    pass


@router.post("/set-pay-referal-level")
async def set_pay_refs_level(request: mains_models.RefsLevel):
    """
    Список уровней реферальной программы
    :param id:
    :return:
    """
    pass


@router.get("/get-pay-referal-level/{id}")
async def get_pay_refs_level(id: int):
    """
    Список уровней реферальной программы
    :param id:
    :return:
    """
    pass


@router.put("/update-pay-referal-level")
async def update_pay_refs_level(request: mains_models.RefsLevel):
    """
    Изменить уровни реферальной программы
    :param id:
    :return:
    """
    pass


@router.delete("/delete-pay-referal-level")
async def delete_pay_refs_level(request: mains_models.RefsLevel):
    """
    Изменить уровни реферальной программы
    :param id:
    :return:
    """
    pass

