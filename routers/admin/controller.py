import mysql.connector as cpy
import config
import routers.admin.models as admin_models


async def check_access(request: admin_models.AuthRoles):
    print("user", request)
    if request.user_id != 1:

        return {"Success": False, "data": "Пользователь не имеет прав на выполнение данного метода"}
    return request.user_id
    # user_id_check = False
    #
    # print(user_id, method_id, page_id)
    # with cpy.connect(**config.config) as cnx:
    #     with cnx.cursor() as cur:
    #         data_string = "SELECT FROM user where id = '" + str(user_id) + "'"
    #
    # if user_id_check:
    #     print("тут")
    #     return {"Success": False, "data": "Пользователь не имеет прав на выполнение данного метода"}
    # return {"Success": False, "data": user_id}


async def send_link_to_user(user_id):
    with cpy.connect(**config.config) as cnx:
        with cnx.cursor() as cur:
            # try todo
            data_string = "SELECT FROM user where id = '" + str(user_id) + "'"
            cur.execute(data_string)
            data = cur.fetchone()
            if data:
                string = "UPDATE user SET banned = 0 where id = '" + str(user_id) + "'"
                cur.execute(string)
                cnx.commit()
                return {"Success":True, "data": "Пользователь подтвержден"}
            cur.close()
    return {"Success":False, "data": "Пользователь подтвержден"}
