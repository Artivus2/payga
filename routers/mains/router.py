import routers.mains.models as mains_models
from fastapi import APIRouter, HTTPException
from routers.mains.controller import (
    get_bank,
    get_chart,
    get_curr,
    get_reqs_by_user,
    get_reqs_groups_by_id,
    req_by_filters,
    set_reqs_by_any,
    set_reqs_group_by_any,
    get_automation_history,
    get_automation_status,
    get_pay_reqs_status_by_id,
    get_pay_reqs_types_by_id,
    get_turn_off
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


@router.post("/get-reqs")
async def get_reqs(request: mains_models.Reqs):
    """
    Запрос реквизитов пользователя по user_id
    :param request:
    :param dict:
    :return:

    """
    response = await get_reqs_by_user(request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-reqs")
async def set_reqs(request: mains_models.Reqs):
    """
    установка реквизитов пользователя
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
        print(k, v)
        if v is not None:
            payload[k] = v
    response = await set_reqs_by_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
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
    print(response)
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
        print(k, v)
        if v is not None:
            payload[k] = v
    response = await set_reqs_group_by_any(payload)
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
    :param id: 0 - все
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

