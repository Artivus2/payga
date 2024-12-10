import json
from pydantic import BaseModel
from starlette.requests import Request
from fastapi import APIRouter, HTTPException, Depends
from routers.akktest.models import SimpleDep
import routers.user.models as user_models

router = APIRouter(prefix='/api/v1/akktest', tags=['Тестовая'], dependencies=[Depends(SimpleDep())])


# query=f"""INSERT INTO codes(email,reset_code,status,expired_in)
#                 VALUES ('{request.email}','{reset_code}',1,'{(datetime.now()+timedelta(hours=8))}');"""

@router.post("/test1")
async def root1(request: user_models.User):

    return {"test1": request}
