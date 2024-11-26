import json
from pydantic import BaseModel
from starlette.requests import Request
from fastapi import APIRouter, HTTPException, Depends
from routers.akktest.models import SimpleDep


router = APIRouter(prefix='/api/v1/akktest', tags=['Тестовая'], dependencies=[Depends(SimpleDep())])


# query=f"""INSERT INTO codes(email,reset_code,status,expired_in)
#                 VALUES ('{request.email}','{reset_code}',1,'{(datetime.now()+timedelta(hours=8))}');"""

class Users(BaseModel):
    user_id: int


@router.post("/test1")
async def root1(user_id: Users):

    return {"test1": user_id}
