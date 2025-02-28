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


class Invoice(BaseModel):
    __table_name__ = "pay_invoice"
    id: int | None = None
    req_id: int | None = None
    sum_fiat: float | None = None
    api_key: str | None = None


class FavReqsTypes(BaseModel):
    __table_name__ = "pay_fav_merchant_reqs_types"
    id: int | None = None
    shop_id: int | None = None
    pay_reqs_types_id: int | None = None
    active:  int | None = None



class Shops(BaseModel):
    __table_name__ = "pay_shops"
    id: int | None = None
    uuid: str | None = None
    user_id: int | None = None
    title: str | None = None
    site_url: str | None = None
    balance: float | None = None
    date: str | None = None
    success_url: str | None = None
    fail_url: str | None = None
    secret_word: str | None = None


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


class FundsHistory(BaseModel):
    __table_name__ = "pay_history"
    id: int | None = None
    user_id: int | None = None
    np_order_uuid: str | None = None
    value: float | None = None
    date: str | None = None
    status: str | None = None
