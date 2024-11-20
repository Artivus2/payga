import json
import routers.mains.models as mains_models
import requests
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix='/api/v1/mains', tags=['Mains'])

