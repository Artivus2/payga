import routers.admin.models as admin_models
from fastapi import APIRouter, HTTPException
from routers.admin.controller import send_link_to_user
from routers.admin.utils import send_email_yii2

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
    if await send_link_to_user(request.user_id):
        await send_email_yii2(request.login, request.email)


    # send link todo