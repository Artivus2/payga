import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.orders.router import router as router_orders
from routers.user.router import router as router_user
from routers.admin.router import router as router_admin
from routers.actives.router import router as router_actives
from routers.mains.router import router as router_mains
from routers.roles.router import router as router_roles
from routers.stats.router import router as router_stats
from routers.nowpayments.router import router as nowpayements


app = FastAPI()


# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

# @app.get("/")
# async def route():
#     return {
#         "message": "Сайт находится в разработке!"
#     }

# @app.get("/register/{referral_code}")
# async def register_with_referral_code(referral_code: str | None):
#     """
#     регистрация по реферальной ссылке
#     http://test.greenavi.com/24g23g24g2
#     :param referral_code:
#     :return:
#     """
#     print(referral_code)
#     return referral_code


app.include_router(router_user)
app.include_router(router_orders)
app.include_router(router_admin)
app.include_router(router_actives)
app.include_router(router_mains)
app.include_router(router_roles)
app.include_router(router_stats)
app.include_router(nowpayements)
# и еще todo


async def main():
    config = uvicorn.Config("main:app", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
