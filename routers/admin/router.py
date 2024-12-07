import routers.admin.models as admin_models
import routers.user.models as users_models
from fastapi import APIRouter, HTTPException, Depends
from routers.admin.controller import (
    send_link_to_user,
    check_access,
    get_all_users_profiles,
    get_all_roles,
    crud_roles,
    change_user_role,
    set_users_any
)
from routers.admin.utils import send_email

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


@router.post("/sms-data")
async def sms_receiver(request: admin_models.Sms):
    """
    SMS Receiver
    :param request:
    :param id:
    :return:
    """
    print(request)
    return True




