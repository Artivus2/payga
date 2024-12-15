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