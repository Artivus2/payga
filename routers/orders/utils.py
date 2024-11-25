import uuid


async def generate_uuid() -> str:
    uuid_number = uuid.uuid4()
    return str(uuid_number)


async def get_course(chart_id):
    #todo получить курс usdtrub
    return 100