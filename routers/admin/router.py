import routers.admin.models as admin_models
from fastapi import APIRouter, HTTPException, Depends
from routers.admin.controller import send_link_to_user, check_access
from routers.admin.utils import send_email_yii2
from typing import Annotated


router = APIRouter(prefix='/api/v1/admin', tags=['Admin'])


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
            detail=response.json(),
        )
    await send_email_yii2(request.login, request.email)


@router.post("/create-role")
async def create_role(request: admin_models.AuthRoles):
    """
    Создать роль
    :param item:
    :param id:
    :param request:
    :return:
    """
    print(request)
    return request


@router.post("/get-role")
async def get_role(request: admin_models.AuthRoles):
    """
    Получить роль
    :param commons:
    :param user_id:
    :param result:
    :param item:
    :param id:
    :param request:
    :return:
    """
    return request



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
    pass


@router.post("/delete-role")
async def delete_role(request: admin_models.Role):
    """
    Удалить роль
    id: int
    title: str
    pages: list
    status: int
    :return:
    """
    pass


@router.post("/create-auth-roles")
async def create_role(request: admin_models.AuthRoles):
    """
    Создать привязку user-role-method-pages
    :param request:
    :return:
    """
    pass


@router.get("/get-auth-roles/{id}")
async def get_role(id: int):
    """
    получить привязку user-role-method-pages по id
    :param id:
    :return:
    """
    pass


@router.post("/set-auth-roles")
async def update_role(request: admin_models.AuthRoles):
    """
    Изменить привязку user-role-method-pages
    :param request:
    :return:
    """
    pass


@router.post("/delete-auth-roles")
async def delete_role(request: admin_models.AuthRoles):
    """
    удалить привязку user-role-method-pages по id
    :param request:
    :return:
    """
    pass