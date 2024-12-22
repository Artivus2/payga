import os
import shutil
from typing import Annotated
from fastapi import APIRouter, Response, Depends, UploadFile, File, HTTPException, Form, Body, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.responses import FileResponse
import routers.orders.models as orders_models
import base64
from routers.orders.controller import (
    create_order_for_user,
    get_orders_by_any,
    delete_order_by_id,
    update_order_by_id,
    insert_docs,
    get_docs_urls,
    create_new_cashback_for_group,
    set_cashback_status_for_group_by_id,
    set_cashback_to_group,
    get_all_cashback_statuses,
    get_all_cashback_by_id


)



router = APIRouter(prefix='/api/v1/orders', tags=['Ордера'])


# @router.post("/create-order")
# async def create_order(request: orders_models.Orders):
#     """
#     Создать ордер
#     :return:
#     """
#     response = await create_order_for_user(request)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     print(response)
#     return response


@router.post("/get-orders")
async def order_filters(request: orders_models.Orders):
    """
    фильтры по ордерам
    :param request:
    :return:
    """
    payload = {}
    for k, v in request:
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


# @router.get("/get-order-status/{id}")
# async def get_order(id: int):
#     """
#     Получить статус ордера по id из pay_notify_order_types
#     :return:
#     """
#     response = await get_order_status_by_id(id)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     print(response)
#     return response


@router.post("/set-order-status")
async def update_order(request: orders_models.Orders):
    """
    Обновить статус ордера по id и pay_notify_order_types_id
    :return:
    """
    if request.docs_id is None:
        request.docs_id = 0
    print(request)
    response = await update_order_by_id(request.id, request.pay_notify_order_types_id, request.docs_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response


@router.post("/delete-order")
async def delete_order(request: orders_models.Orders):
    """
    Удалить ордер в статус удален 26
    :param request:
    :param response:
    :return:
    """
    response = await delete_order_by_id(request.id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response



@router.post("/order-docs-load")
async def store(order_uuid: int = Form(...), image: UploadFile = File(...)):
    """
    Записываем urls платежек по order_id
    :param order_id:
    :param image:
    :return:
    """
    #files: List[UploadFile] = File(...)
    #[file.filename for file in files]
    #images = []
    file_location = f"files/{image.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
        full_path_url = "/" + str(file_location)
        #images.append(full_path_url)
        response = await insert_docs(order_uuid, image.filename)
        if not response['Success']:
            raise HTTPException(
                status_code=400,
                detail=response
            )
        print(response)
        return response





@router.get("/get-orders-docs-ids/{order_id}")
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
    filename = response["data"][0]['url']
    print(filename)
    if response["data"][0]['url'].endswith((".jpg", ".jpeg", ".png", ".gif")):
        file_path = os.path.join("\\files", filename)
        #image_url = f"c:\\projects\\payga{file_path}" #wtest
        image_url = f"/var/www/html/psyga{file_path}" #prod
        print(FileResponse(image_url, media_type="image/png"))
        return FileResponse(image_url)




@router.post("/create-cashback")
async def create_cashback(request: orders_models.Cashback):
    """
        # создать вид кешбека на группу
        :param request:
        :return:
    """
    payload = {
        "title": request.title,
        "date": request.date,
        "pay_reqs_group_id": request.pay_reqs_group_id,
        "value": request.value,
        "status_id": request.status_id
    }
    response = await create_new_cashback_for_group(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/set-cashback-percent-for-group")
async def set_cashback(id: int, value: int):
    """
    # поменять % кешбека группе
    :param request:
    :return:
    """
    response = await set_cashback_to_group(id, value)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/set-cashback-status-for-group")
async def set_cashback_status_for_group(request: orders_models.Cashback):
    """
    поменять статус кешбека группе (действует недействует) ?
    status: действует, не действует
    :param request:
    :return:
    """
    response = await set_cashback_status_for_group_by_id(request.id, request.status_id)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/get-cashback-status")
async def get_cashback_status(request: orders_models.CashbackStatus):
    """
    получить список статусов кешбека
    status: действует, не действует
    :param id:
    :return:
    """
    response = await get_all_cashback_statuses(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response


@router.post("/get-all-cashbacks")
async def get_all_cashback(request: orders_models.Cashback):
    """
    получить список статусов кешбека
    status: действует, не действует
    :param request:
    :return:
    """
    response = await get_all_cashback_by_id(request)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
    return response

