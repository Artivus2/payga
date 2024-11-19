import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.orders.router import router as router_orders
from routers.user.router import router as router_user

app = FastAPI()


# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.get("/")
async def route():
    return {
        "message": "Сайт находится в разработке!"
    }
app.include_router(router_user)
app.include_router(router_orders)
# и еще todo


async def main():
    config = uvicorn.Config("main:app", port=5001, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
