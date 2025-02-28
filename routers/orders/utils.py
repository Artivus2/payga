import uuid
from fastapi import HTTPException
import requests


async def generate_uuid() -> str:
    uuid_number = uuid.uuid4()
    return str(uuid_number)


async def get_course():

    api_url = "https://www.cbr-xml-daily.ru/daily_json.js"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    result = response.json()
    resp = {"data": {"amount": result["Valute"]['USD']['Value']}}
    print(resp)

    return resp

#get_course()