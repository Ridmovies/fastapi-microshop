from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


from items_views import router as items_route
from users.views import router as users_route
from api_v1.orders.router import router as orders_router
from api_v1.products.views import router as products_route
from api_v1.demo_auth.router import router as demo_route
from api_v1.demo_auth.demo_jwt_auth import router as demo_jwt_auth_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(demo_jwt_auth_route)
app.include_router(items_route, prefix="/items", tags=["items"])
app.include_router(users_route, prefix="/users", tags=["users"])
app.include_router(products_route, prefix="/products", tags=["products"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(demo_route, prefix="/demo_auth", tags=["demo_auth"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
