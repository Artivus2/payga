import os
import shutil
from fastapi import APIRouter, Response, Depends, UploadFile, File, HTTPException, Form, Body, Query
from fastapi.responses import FileResponse
import routers.orders.models as orders_models
from routers.admin.utils import generate_code
from routers.orders.controller import (
    get_orders_by_any,
    delete_order_by_id,
    update_order_by_any,
    insert_docs,
    get_docs_urls,
    create_new_cashback_for_group,
    set_cashback_status_for_group_by_id,
    set_cashback_to_group,
    get_all_cashback_statuses,
    get_all_cashback_by_id,
    payout_reqs
)



router = APIRouter(prefix='/api/v1/orders', include_in_schema=False, tags=['Ордера'])


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
    return response


@router.post("/set-order-status")
async def update_order(request: orders_models.Orders):
    """
    Обновить статус ордера по любым параметрам
    :return:
    """
    payload = {}
    for k, v in request:
        if v is not None:
            payload[k] = v
    print(request)
    response = await update_order_by_any(payload)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    return response

@router.get("/get-payout-orders-reqs/{order_uuid}")
async def order_payout_info(order_uuid: str):
    """
    для не принятых ордеров payout
    """
    response = await payout_reqs(order_uuid)
    if not response['Success']:
        raise HTTPException(
            status_code=400,
            detail=response
        )
    print(response)
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
    dop_kod = str(await generate_code(8)) + "_" + image.filename
    file_location = f"files/pays/{dop_kod}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
        full_path_url = "/" + str(file_location)
        #images.append(full_path_url)
        response = await insert_docs(order_uuid, dop_kod)
        print(response)
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
        #file_path = os.path.join("\\files", filename)
        file_path = os.path.join("/files/pays", filename)
        #image_url = f"c:\\projects\\payga{file_path}" #wtest
        image_url = f"/var/www/html/payga{file_path}" #prod
        return FileResponse(image_url)




# @router.post("/create-cashback")
# async def create_cashback(request: orders_models.Cashback):
#     """
#         # создать вид кешбека на группу
#         :param request:
#         :return:
#     """
#     payload = {
#         "title": request.title,
#         "date": request.date,
#         "pay_reqs_group_id": request.pay_reqs_group_id,
#         "value": request.value,
#         "status_id": request.status_id
#     }
#     response = await create_new_cashback_for_group(payload)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     print(response)
#     return response


# @router.post("/set-cashback-percent-for-group")
# async def set_cashback(id: int, value: int):
#     """
#     # поменять % кешбека группе
#     :param request:
#     :return:
#     """
#     response = await set_cashback_to_group(id, value)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     print(response)
#     return response

#
# @router.post("/set-cashback-status-for-group")
# async def set_cashback_status_for_group(request: orders_models.Cashback):
#     """
#     поменять статус кешбека группе (действует недействует) ?
#     status: действует, не действует
#     :param request:
#     :return:
#     """
#     response = await set_cashback_status_for_group_by_id(request.id, request.status_id)
#     if not response['Success']:
#         raise HTTPException(
#             status_code=400,
#             detail=response
#         )
#     print(response)
#     return response


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


