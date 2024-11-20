import json
import routers.roles.models as roles_models
import requests
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix='/api/v1/roles', tags=['Roles'])