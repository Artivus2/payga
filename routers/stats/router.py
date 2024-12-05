import json
import routers.stats.models as stats_models
import requests
from fastapi import APIRouter, HTTPException
from routers.stats.controller import get_all_stat


router = APIRouter(prefix='/api/v1/stats', tags=['Статистика'])


@router.post("/get-all-stat")
async def get_stats(request: stats_models.Statistic):
    """

    :param request:
    :return:
    """
    response = await get_all_stat(request.user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response