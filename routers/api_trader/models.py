from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from routers.admin.controller import get_user_from_api_key


class GetApiKey:
    async def __call__(self, request: Request):
        response = await get_user_from_api_key(request.headers.get('x-api-key'))
        if not response['Success']:
            raise HTTPException(
                status_code=404,
                detail="Не авторизован или сессия просрочена"
            )
        return response


class CreatePaymentRequest(BaseModel):
    amount: float | None = None
    currency: str | None = None
    order_id: str | None = None
    pay_currency: str | None = None
    user_id: int | None = None
    type_id: int | None = None


class CreatePayoutRequest(BaseModel):
    amount: float | None = None
    currency: str | None = None
    address: str | None = None
    type_id: int | None = None
    user_id: int | None = None