from fastapi import HTTPException
from starlette.requests import Request
from routers.user.controller import get_token_by_token


def check_db_token(access_token):
    if access_token:
        response = get_token_by_token(access_token)
        if not response['Success']:
            raise HTTPException(
                status_code=404,
                detail=response
            )
        return response


class SimpleDep:
    async def __call__(self, request: Request):
        response = await get_token_by_token(request.headers.get('authorization'))
        if not response['Success']:
            raise HTTPException(
                status_code=404,
                detail="Не авторизован или сессия просрочена"
            )
        print(response)
        return response
