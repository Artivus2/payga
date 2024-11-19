
from fastapi import APIRouter, Response
from routers.orders.utils import generate_uuid




router = APIRouter(prefix='/api/v1/orders', tags=['Orders'])


@router.get("/create-order")
async def create_order():
    """

    :return:
    """
    uuids = await generate_uuid()
    #print(uuids)
    return uuids

@router.post("/read-order")
async def read_order():
    """

    :return:
    """
    pass


@router.post("/update-order")
async def update_order():

    pass


@router.post("/delete-order")
async def delete_order(response: Response):
    """

    :param response:
    :return:
    """

    pass

