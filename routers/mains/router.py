import routers.mains.models as mains_models
from fastapi import APIRouter, HTTPException
from routers.mains.controller import (
    get_bank,
    set_fav_bank,
    get_chart,
    get_curr,
    get_reqs_groups_by_id,
    req_by_filters,
    set_reqs_by_any,
    set_reqs_group_by_any,
    remove_reqs_by_id,
    get_automation_history,
    get_automation_status,
    get_automation_type,
    get_pay_reqs_status_by_id,
    get_pay_reqs_types_by_id,
    set_pay_reqs_types_by_id,
    remove_pay_reqs_types_by_id,
    get_turn_off,
    create_reqs_for_user,
    create_reqs_group,
    add_reqs_by_id_to_group,
    remove_reqs_by_id_from_group,
    remove_group_by_id,
    get_pay_refs_types_by_id,
    set_or_create_pay_refs_types_by_id,
    get_pay_refs_levels_by_id,
    update_pay_refs_level_by_id,
    get_pay_refs_by_user,



)

router = APIRouter(prefix='/api/v1/mains', tags=['Основные'])

@router.get("/get-banks/{id}")
async def get_bank_by_id(id: str):
    """
    Запрос банка
    :param id:
    :param token:
    :return:
    token
    """

    response = await get_bank(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-favorite-banks")
async def set_banks(request: mains_models.BankFavs):
    """
    Запрос банка
    :param request:
    :param token:
    :return:
    token
    """

    response = await set_fav_bank(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-chart/{id}")
async def get_chart_by_id(id: int):
    """
    Запрос крипты
    :param id:
    :param chart:
    :return:

    """
    print(id)
    response = await get_chart(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-currency/{id}")
async def get_currency(id: int):
    """
    Запрос крипты
    :param id:
    :param chart:
    :return:

    """
    response = await get_curr(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/create-reqs")
async def create_reqs(request: mains_models.Reqs):
    """
    Создать реквизиты пользователя
    :param request:
    :return:
    """
    response = await create_reqs_for_user(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-reqs")
async def set_reqs(request: mains_models.Reqs):
    """
    смена реквизитов пользователя
    user_id: int
    req_group_id: int по умлочанию 0 не добавлен ни в какую группу\n
    sequence: int частота использования по умолчанию 0
    pay_pay_id: int из запроса /api/v1/actives/get-pay-type/{id} 0 - все
    value: str здесь номер карты счета
    currency_id: int  по умолчанию рубль 1
    reqs_types_id: int       /api/v1/mains/get-pay-reqs-types/{id}  0 - все типы
    reqs_status_id: int      /api/v1/mains/get-pay-reqs-types/{id}  0 - все статусы
    bank_id: int      /api/v1/mains/get-banks/{id}, 0 - все банки
    chart_id: int     /api/v1/mains/get-chart/{id}, 0 - все криптовалют (259 - usdt)
    phone: str  телефон
    qty_limit_hour: int лимиты в час
    qty_limit_day: int
    qty_limit_month: int
    sum_limit_hour: float сумма лимитов в час
    sum_limit_day: float
    sum_limit_month: float

    :param request:
    :param dict:
    :return:
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await set_reqs_by_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-reqs")
async def remove_reqs(request: mains_models.Reqs):
    """
    Удаление реквизитов по ид
    :param request:
    :return:
    """
    response = await remove_reqs_by_id(request.id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response

@router.post("/get-reqs")
async def filter_reqs(request: mains_models.ReqsFilters):
    """
    Запрос реквизитов пользователя по параметрам
    :param request:
    :param dict:
    :return:

    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await req_by_filters(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/create-reqs-groups")
async def create_reqs_groups(request: mains_models.ReqGroups):
    """
    Создать группу реквизитов
    :param request:
    title: str
    types_automate_id: int () /get-automation-type/{id} 1 - Ручной, 2 - автоматический
    turn_off: int /get-pay-reqs-turn-off/{id} 0 - выключено, 1 - включено
    :return:
    """
    response = await create_reqs_group(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/get-reqs-groups/{id}")
async def get_reqs_groups(id: int):
    """
    Запрос реквизитов группы
    :param id:
    :param request:
    :param dict:
    :return:
    """
    response = await get_reqs_groups_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-reqs-groups")
async def set_reqs_groups(request: mains_models.ReqGroups):
    """
    Установка реквизитов группы
    :param request:
    :param dict:
    :return:
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await set_reqs_group_by_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response

@router.post("/add-reqs-to-group")
async def add_reqs_to_group(request: mains_models.ReqToGroups):
    """
    Добавить реквизит в группу
    :param request:
    :return:
    """
    response = await add_reqs_by_id_to_group(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-reqs-from-group")
async def remove_reqs_from_group(request: mains_models.ReqToGroups):
    """
    Удалить реквизит из группы
    :param request:
    :return:
    """
    response = await remove_reqs_by_id_from_group(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-group-by-id")
async def remove_group(request: mains_models.Reqs):
    """
    удалить группу и обнулить реквизиты
    user_id
    req_group_id
    :param request:
    :return:
    """
    response = await remove_group_by_id(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-automation-history/{id}")
async def get_pay_automation_history(request: mains_models.AutomationHistory):
    """
    Запрос типов автоматизации
    :param request:
    :param dict:
    :return:
    """
    response = await get_automation_history(request.id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-automation-status/{id}")
async def get_pay_automation_status(id: int):
    """
    Запрос статусов автоматизации
    :param id: 0 - все Активные, Успешные, Ошибка, Ошибка шаблона
    :param request:
    :param dict:
    :return:
    """
    response = await get_automation_status(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-automation-type/{id}")
async def get_pay_automation_type(id: int):
    """
    автоматическое выключение реквизитов без доступа к автоматике (1 - ручной, 2 - автоматический)
    :param request:
    :param dict:
    :return:
    """
    response = await get_automation_type(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-reqs-turn-off/{id}")
async def get_pay_automation_turn_off(id: int):
    """
    автоматическое выключение реквизитов без доступа к автоматике (1 - включено, 0 - выключено)
    :param request:
    :param dict:
    :return:
    """
    response = await get_turn_off(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



@router.get("/get-pay-reqs-status/{id}")
async def get_pay_reqs_status(id: int):
    """
    Запрос статусов реквизитов
    :param id: 0 - все
    :param request:
    :param dict:
    :return:
    """
    response = await get_pay_reqs_status_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-reqs-types/{id}")
async def get_pay_reqs_types(id: int):
    """
    Запрос типов реквизитов
    :param id: 0 - все
    :param request:
    :param dict:
    :return:
    """
    response = await get_pay_reqs_types_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-pay-reqs-types")
async def get_pay_reqs_types(request: mains_models.ReqsTypes):
    """
    Платежные методы
    :param request:
    :return:
    """
    response = await set_pay_reqs_types_by_id(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-pay-reqs-types")
async def remove_pay_reqs_types(request: mains_models.ReqsTypes):
    """
    Платежные методы
    :param request:
    :return:
    """
    response = await remove_pay_reqs_types_by_id(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


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
    response = await get_pay_refs_types_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-pay-referal-types/{id}")
async def set_pay_refs_types(request: mains_models.Refs):
    """
    Типы рефералов
    :param
    request:
    :param
    dict:
    :return:
    """
    response = await set_or_create_pay_refs_types_by_id(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-referal/{user_id}")
async def get_pay_refs(user_id: int):
    """
    Рефералы по user_id
    :param
    request:
    :param
    dict:
    :return:
    """
    response = await get_pay_refs_by_user(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response



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
    response = await get_pay_refs_levels_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.put("/update-pay-referal-level")
async def update_pay_refs_level(request: mains_models.RefsLevel):
    """
    Изменить уровни реферальной программы
    :param id:
    :return:
    """
    response = await update_pay_refs_level_by_id(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.delete("/delete-pay-referal-level")
async def delete_pay_refs_level(request: mains_models.RefsLevel):
    """
    Изменить уровни реферальной программы
    :param id:
    :return:
    """
    pass

