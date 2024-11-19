import mysql.connector as cpy
import config


async def send_link_to_user(user_id) -> bool:
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
                return True
            cur.close()
    return False
