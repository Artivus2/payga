
from fastapi import APIRouter, Response, Depends, UploadFile, File
from routers.orders.utils import generate_uuid
import json
import routers.orders.models as orders_models
import requests




router = APIRouter(prefix='/api/v1/orders', tags=['Orders'])


@router.post("/create-order")
async def create_order():
    """

    :return:
    """
    uuids = await generate_uuid()
    #print(uuids)
    return uuids

@router.get("/read-order")
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

@router.post("/order-docs-load")
def store(data: orders_models.Docs = Depends(), image: UploadFile = File(...)):
    data_received = data.dict()

    return {"message": data_received['id'], "image_filename": image.filename}