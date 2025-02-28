import os
import shutil

from starlette.responses import FileResponse

import routers.mains.models as mains_models
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from routers.mains.controller import (
    get_banks,
    set_admin_bank,
    get_fav_bank,
    set_fav_bank,
    remove_fav_bank,
    remove_admin_bank,
    get_chart,
    get_curr,
    get_reqs_groups_by_id,
    get_payout_reqs,
    req_by_filters,
    set_reqs_by_any,
    set_reqs_group_by_any,
    remove_reqs_by_id,
    get_automation_history,
    get_automation_status,
    get_automation_type,
    get_pay_reqs_status_by_id,
    get_pay_reqs_types_by_id,
    get_urls_reqs,
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
    set_parsers,
    get_all_parsers,
    set_messages,
    insert_check,
    get_messages_by_any,
    get_message_url,
    set_message_status




)

router = APIRouter(prefix='/api/v1/mains', include_in_schema=False, tags=['Основные'])

@router.get("/get-admin-banks/{active}")
async def get_admin_fav(active: int):
    """
    Запрос банков админа
    :param user_id:
    :param token:
    :return:
    token
    """

    response = await get_banks(active)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-fav-banks/{user_id}")
async def get_fav_bank_by_id(user_id: int):
    """
    Запрос банка пользователя fav_banks
    :param user_id:
    :param token:
    :return:
    token
    """

    response = await get_fav_bank(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-admin-banks")
async def set_admin_banks(request: mains_models.BankAdm):
    """
    Создать список банков для реквизитов админа
    :param request:
    :param token:
    :return:
    token
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await set_admin_bank(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/set-favorite-banks")
async def set_fav_banks(request: mains_models.BankFavs):
    """
    Создать список банков для реквизитов из админа ACTIVE = 1 / 0
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


@router.post("/remove-favorite-banks")
async def remove_banks(request: mains_models.BankFavs):
    """
    Удалить из списка банков для реквизитов
    :param request:
    :param token:
    :return:
    """
    response = await remove_fav_bank(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/remove-admin-banks")
async def remove_banks(request: mains_models.BankAdm):
    """
    Удалить из списка банков админа для реквизитов
    :param request:
    :param token:
    :return:
    """
    response = await remove_admin_bank(request)
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
    bank_id: int      /api/v1/mains/get-fav-banks/{id}, 0 - все банки
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


@router.post("/get-payout-reqs/{order_id}")
async def filter_reqs(order_id: int):
    """
    реквизиты для вывода пользователей если не нзанчаен payout
    """
    response = await get_payout_reqs(order_id)
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



@router.get("/get-reqs-groups/{user_id}")
async def get_reqs_groups(user_id: int):
    """
    Запрос реквизитов группы (0 - для админа все)
    :param id:
    :param request:
    :param dict:
    :return:
    """
    response = await get_reqs_groups_by_id(user_id)
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


@router.post("/set-parsers")
async def set_parss(request: mains_models.Parsers):
    """
    получить все парсеры по банкам
    :param id:
    :return:
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await set_parsers(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-parsers")
async def get_parsers():
    """
    получить все парсеры по банкам
    :param id:
    :return:
    """
    response = await get_all_parsers()
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-pay-reqs-png/{id}")
async def get_reqs_urls(id: int):
    """
    получаем png rqs_types
    :param request:
    :return:
    """
    response = await get_urls_reqs(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    filename = response["data"]
    print(filename)
    if response["data"].endswith((".jpg", ".jpeg", ".png", ".gif", ".svg")):
        #file_path = os.path.join("\\files", filename)
        file_path = os.path.join("/files", filename)
        #image_url = f"c:\\projects\\payga{file_path}" #wtest
        image_url = f"/var/www/html/payga{file_path}" #prod
        return FileResponse(image_url)


@router.post("/create-message")
async def create_message(request: mains_models.Messages):
    """
    id: int | None = None
    order_uuid: str | None = None
    text: str | None = None
    docs_url: str | None = None
    status: int | None = None
    email: str | None = None
    """
    response = await set_messages(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/update-message-status")
async def create_message(request: mains_models.Messages):
    """
    status: int | None = None
    """
    response = await set_message_status(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response

@router.post("/create-message-upload")
async def store(message_uuid: str = Form(...), image: UploadFile = File(...)):
    """
    Записываем urls платежек по order_uuid
    :param order_uuid:
    :param image:
    :return:
    """
    file_location = f"files/{image.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
        response = await insert_check(message_uuid, image.filename)
        if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
        return response


@router.get("/get-message-docs-ids/{message_uuid}")
async def get_message_image(message_uuid: str):
    """
    получаем список платежек по uuid message
    :param request:
    :return:
    """
    response = await get_message_url(message_uuid)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    filename = response["data"]['docs_url']
    print(filename)
    if response["data"]['docs_url'].endswith((".jpg", ".jpeg", ".png", ".gif")):
        #file_path = os.path.join("\\files", filename)
        file_path = os.path.join("/files", filename)
        #image_url = f"c:\\projects\\payga{file_path}" #wtest
        image_url = f"/var/www/html/payga{file_path}" #prod
        return FileResponse(image_url)

@router.post("/get-messages")
async def message_filters(request: mains_models.Messages):
    """
    фильтры по сообщениям
    :param request:
    :return:
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await get_messages_by_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response