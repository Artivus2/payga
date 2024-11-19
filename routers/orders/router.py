
from fastapi import APIRouter, Response
from routers.orders.utils import generate_uuid




router = APIRouter(prefix='/api/v1/orders', tags=['Orders'])


@router.get("/add")
async def add_order():
    uuids = await generate_uuid()
    #print(uuids)
    # user = await UsersDAO.find_one_or_none(session=session, filters=EmailModel(email=user_data.email))
    # if user:
    #     raise UserAlreadyExistsException
    # user_data_dict = user_data.model_dump()
    # del user_data_dict['confirm_password']
    # await UsersDAO.add(session=session, values=SUserAddDB(**user_data_dict))
    # return {'message': f'Вы успешно зарегистрированы!'}
    return uuids


@router.post("/modify")
async def modify_order():
    # check = await authenticate_user(session=session, email=user_data.email, password=user_data.password)
    # if check is None:
    #     raise IncorrectEmailOrPasswordException
    # access_token = create_access_token({"sub": str(check.id)})
    # response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    # return {'ok': True, 'access_token': access_token, 'message': 'Авторизация успешна!'}
    pass


@router.post("/delete")
async def delete_order(response: Response):
    # response.delete_cookie(key="users_access_token")
    # return {'message': 'Пользователь успешно вышел из системы'}
    pass

