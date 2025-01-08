import json
import routers.stats.models as stats_models
import requests
from fastapi import APIRouter, HTTPException

from routers.orders.utils import get_course
from routers.stats.controller import (
    get_all_stat_payin,
    get_all_stat_payout,
    get_stat_by_day_payin,
    get_stat_by_day_payout
)


router = APIRouter(prefix='/api/v1/stats', include_in_schema=False, tags=['Статистика'])


@router.get("/get-all-stat-payin/{user_id}")
async def get_stats(user_id: int):
    """

    :param request:
    :return:
    """
    response = await get_all_stat_payin(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.get("/get-all-stat-payout/{user_id}")
async def get_stats(user_id: int):
    """

    :param request:
    :return:
    """
    response = await get_all_stat_payout(user_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/get-stat-by-day-payin")
async def get_stats(stat: stats_models.Statistic):
    """
    :param request:
    user_id:
    title:
    date_begin:
    date_end:
    pay_id:
    :return:
    """
    response = await get_stat_by_day_payin(stat)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/get-stat-by-day-payout")
async def get_stats(stat: stats_models.Statistic):
    """
    :param request:
    user_id:
    title:
    date_begin:
    date_end:
    pay_id:
    :return:
    """
    response = await get_stat_by_day_payout(stat)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


