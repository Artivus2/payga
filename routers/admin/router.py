import json
import datetime

from starlette.requests import Request
import re
import routers.admin.models as admin_models
import routers.user.models as users_models
import routers.actives.models as actives_models
from fastapi import APIRouter, HTTPException, Depends
import routers.orders.models as orders_models
from routers.admin.controller import (
    send_link_to_user,
    check_access,
    get_all_users_profiles,
    get_all_roles,
    crud_roles,
    change_user_role,
    set_users_any,
    create_invoice_data,
    create_sms_data,
    get_user_from_api_key,
    get_info_for_invoice,
    get_pattern,
    check_order_by_id_payin,
    check_order_by_id_payout,
    confirm_deposit_to_balance,
    confirm_balance_to_network

)
from routers.admin.utils import (
    send_email,
)
from routers.orders.controller import update_order_by_id

router = APIRouter(prefix='/api/v1/admin', tags=['Администратор'])


@router.post("/confirm-request")
async def confirm_request(request: admin_models.ConfirmRegister):
    """
    Подтверждение регистрации админом
    Args: Подтверждение
        request: Логин

    Returns:
        Успешно

    """
    response = await send_link_to_user(request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response
    #await send_email(request.email)



@router.post("/get-all-roles")
async def get_roles(request: admin_models.Role):
    """
    Получить роль
    id: int
    :param request:
    :return:
    """
    response = await get_all_roles(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.post("/create-role")
async def create_role(request: admin_models.Role):
    """
    Создать роль
    title: str (unique)
    pages: int
    status: int
    :return:
    """
    response = await crud_roles("create", request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response



@router.post("/update-role")
async def set_role(request: admin_models.Role):
    """
    Изменить роль
    id: int
    title: str
    pages: list
    status: int
    :return:
    """
    response = await crud_roles("set", request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.post("/remove-role")
async def delete_role(request: admin_models.Role):
    """
    Удалить роль
    id: int
    :return:
    """
    response = await crud_roles("remove", request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.post("/set-role-status")
async def set_role_status(request: admin_models.Role):
    """
    Статус роли
    id: int
    status: int
    :return:
    """
    response = await crud_roles("status", request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.post("/update-auth-roles")
async def update_user_role(request: admin_models.AuthRoles):
    """
    Изменить роль пользователю
    :param request:
    :return:
    """
    response = await change_user_role(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.get("/get-admin-role-status/{id}")
async def get_admin_role_status(id: int):
    """
    Статусы ролей
    status: Активна (1), не активна (2)
    :param id:
    :return:
    """
    pass


@router.get("/get-admin-method-status/{id}")
async def get_admin_method_status(id: int):
    """
    Статусы методов
    status: Активна (1), не активна (2)
    :param id:
    :return:
    """
    pass


@router.get("/get-admin-page-status/{id}")
async def get_admin_page_status(id: int):
    """
    Статусы страниц
    status: Активна (1), не активна (2)
    :param id:
    :return:
    """
    pass


@router.post("/get-all-users")
async def get_all_users(request: users_models.User):
    """
    Все пользователи

    :param request:
    :param id:
    :return:
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    response = await get_all_users_profiles(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.post("/set-any-user")
async def set_user(request: users_models.User):
    """
    Установка параметров пользователя
    id: user_id
    login: str
    email: str
    telegram: str
    is_active: int
    role_id: int
    banned: int
    app_id: int
    :param request:
    :return:
    """
    payload = {}
    for k, v in request:
        print(k, v)
        if v is not None:
            payload[k] = v
    response = await set_users_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response,
        )
    return response


@router.get("/get-allowed-status/{id}")
async def get_allowed_status(id: int):
    """
    Доступность роли, метода, страницы
    Доступна (1), Не доступна (0)
    :param id:
    :return:
    """
    pass
#
# @router.get("/get-info-for-invoice/{user_id}")
# async def get_info(user_id: int):
#     """
#     req_group_id: list
#     sum_fiat: float
#     bank_id: int
#     :param request:
#     :return:
#     """
#     response = await get_info_for_invoice(user_id)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response,
#         )
#     return response



# @router.post("/create-invoice")
# async def create_invoice(request: admin_models.Invoice):
#     """
#
#     :param request:
#     :return:
#     """
#     response = await create_invoice_data(request)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response,
#         )
#     return response
#
# @router.post("/confirm-invoice")
# async def update_order(request: orders_models.Orders):
#     """
#     Подтвердить поступление средств статус 3
#     :return:
#     """
#     response = await update_order_by_id(request.id, 3)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     return response





@router.post("/check-payin-order")
async def check_order(request: orders_models.Orders):
    """
    подтверждение заявки или отмена payin
    id
    pay_notify_order_types_id отказ 2 подтверждение 3
    :param request:
    :return:
    """
    print(request)
    response = await check_order_by_id_payin(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/check-payout-order")
async def check_order(request: orders_models.Orders):
    """
    подтверждение заявки или отмена payout
    id
    pay_notify_order_types_id отказ 20 подтверждение 21
    :param request:
    :return:
    """
    print(request)
    response = await check_order_by_id_payout(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/confirm-deposit-withdrawals")
async def check_order_deposit(request: actives_models.Deposit):
    """
    подтверждаем вывод депозита на баланс
    :param request:
    :return:
    """
    response = await confirm_deposit_to_balance(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/confirm-balance-withdrawals")
async def check_order_to_network(request: actives_models.Balance):
    """
    подтверждаем вывод в сеть
    :param request:
    :return:
    """
    response = await confirm_balance_to_network(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response









