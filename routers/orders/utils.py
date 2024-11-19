import uuid


async def generate_uuid() -> str:
    uuid_number = uuid.uuid4()
    return str(uuid_number)