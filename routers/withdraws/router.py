from fastapi import APIRouter
import routers.withdraws.models as withdraws_models


router = APIRouter(prefix='/api/v1/withdraws', tags=['Вывод средств'])


@router.post("/check-balance")
async def get_stats(request: withdraws_models.Withdraws):
    pass


@router.post("/check-deposit")
async def get_stats(request: withdraws_models.Withdraws):
    pass


@router.post("/balance-out")
async def get_stats(request: withdraws_models.Withdraws):
    pass


