from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from src.users.routers import users_routes
from src.mango_product.routers import category_router,mango_product_routes
from src.orders.routers import order_routes


from src.seed.admin_seed import create_admin
from src.admin.routers import admin_routes

from src.utils.db import DB_Session


API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with DB_Session() as db:
        await create_admin(db)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(users_routes, prefix=API_PREFIX)
app.include_router(category_router, prefix=API_PREFIX)
app.include_router(mango_product_routes, prefix=API_PREFIX)

app.include_router(order_routes, prefix=API_PREFIX)

app.include_router(admin_routes, prefix=API_PREFIX)



@app.get("/")
def read_root():
    return {"message": "Welcome to mango project !"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )