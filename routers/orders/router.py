import shutil
from typing import Annotated

from fastapi import APIRouter, Response, Depends, UploadFile, File, HTTPException, Form, Body, Query
from routers.orders.utils import (
    generate_uuid,
    get_course
)
import json
import routers.orders.models as orders_models
import requests
from routers.orders.controller import (
    create_order_for_user,
    get_order_status_by_id,
    get_orders_by_any,
    delete_order_by_id,
    update_order_by_id,
    insert_docs,
    get_docs_urls
)



router = APIRouter(prefix='/api/v1/orders', tags=['Ордера'])


@router.post("/create-order")
async def create_order(request: orders_models.Orders):
    """

    :return:
    """
    uuids = await generate_uuid()

    payload = {
        'uuid': uuids,
        'user_id': request.user_id,
        'sum_fiat': request.sum_fiat,
        'course': get_course(request.chart_id),
        'chart_id': request.chart_id,
        'pay_id': request.pay_id,
        'value': request.value,
        'cashback': request.cashback,
        'date': request.date,
        'date_expiry': request.date_expiry,
        'req_id': request.req_id,
        'pay_notify_order_types_id': request.pay_notify_order_types_id,
        'docs_ids': request.doc_ids
    }

    response = await create_order_for_user(**payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/get-orders")
async def order_filters(request: orders_models.Orders):
    """
    фильтры по ордерам
    :param request:
    :return:
    """
    payload = {}
    for k, v in request:
        print(k, v)
        if v is not None:
            payload[k] = v
    response = await get_orders_by_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.get("/get-order-status/{id}")
async def get_order(id: int):
    """
    Получить статус ордера по id из pay_notify_order_types
    :return:
    """
    response = await get_order_status_by_id(id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.put("/set-order-status")
async def update_order(order_id: int, status: int):
    """
    Обновить статус ордера по order_id и pay_notify_order_types_id
    :return:
    """
    response = await update_order_by_id(order_id, status)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.delete("/delete-order")
async def delete_order(order_id: int):
    """
    Удалить ордер в статус удален
    :param response:
    :return:
    """
    response = await delete_order_by_id(order_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response



@router.post("/order-docs-load")
async def store(order_id: int = Form(...), image: UploadFile = File(...)):
    """
    Записываем urls платежек по order_id
    :param order_id:
    :param image:
    :return:
    """
    #files: List[UploadFile] = File(...)
    #[file.filename for file in files]
    images = []
    file_location = f"files/{image.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
        full_path_url = str(image.filename) + "/" + str(file_location)
        images.append(full_path_url)
        response = await insert_docs(order_id, full_path_url)
        if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
        print(response)
        return response





@router.post("/get-orders-docs-ids/{order_id}")
async def get_docs(order_id: int):
    """
    получаем список платежек по id ордера
    :param request:
    :return:
    """
    response = await get_docs_urls(order_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response



@router.get("/get-cashback/{order_id}")
async def get_cashback(order_id: int):
    """
    получаем список кешбеков по ордеру
    :param request:
    :return:
    """
    pass


@router.put("/set-cashback")
async def set_cashback(order_id: int):
    """
    установить кешбек по ордеру
    :param request:
    :return:
    """
    pass



@router.get("/get-cashback-status/{id}")
async def get_cashback_status(id: int):
    """
    получаем список статусов кешбека
    status: действует, не действует
    :param request:
    :return:
    """
    pass


@router.put("/set-cashback-status")
async def set_cashback_status(id: int):
    """
    Изменить список статусов кешбека
    status: действует, не действует
    :param request:
    :return:
    """
    pass