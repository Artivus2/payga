import json
import routers.stats.models as stats_models
import requests
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix='/api/v1/stats', tags=['Stats'])