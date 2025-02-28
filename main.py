import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from routers.orders.router import router as router_orders
from routers.user.router import router as router_user
from routers.admin.router import router as router_admin
from routers.actives.router import router as router_actives
from routers.mains.router import router as router_mains
from routers.roles.router import router as router_roles
from routers.stats.router import router as router_stats
from routers.nowpayments.router import router as nowpayments
from routers.api_merchant.router import router as merchant
from routers.api_trader.router import router as trader
from routers.api_operator.router import router as operator
from routers.withdraws.router import router as withdraws
from routers.notifications.router import router as notifications


app = FastAPI()

#app.mount("/files", StaticFiles(directory="/var/www/html/payga/files"), name="files")
#IMAGES_DIR = "/var/www/html/payga/files"
# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admin.greenavi.com", "http://localhost:3000", "http://localhost"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
    #allowed_hosts=['greenavi.com', '*.greenavi.com'],

)

@app.get("/files/pay-greenavi.apk")
def download_file():
    folder_path = r"files"
    file_location = f'{folder_path}{os.sep}pay-greenavi.apk'
    return FileResponse(file_location, media_type='application/octet-stream', filename='pay-greenavi.apk')


app.include_router(merchant)
app.include_router(trader)
app.include_router(operator)
app.include_router(router_user)
app.include_router(router_orders)
app.include_router(router_admin)
app.include_router(router_actives)
app.include_router(router_mains)
app.include_router(router_roles)
app.include_router(router_stats)
app.include_router(nowpayments)
app.include_router(withdraws)
app.include_router(notifications)
# и еще todo


async def main():
    config = uvicorn.Config("main:app", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
