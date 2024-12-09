from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.models.base import Base
from core.models.database import init_db
from core.models.db_helper import db_helper
from items_views import router as items_route
from users.views import router as users_route
from api_v1.products.views import router as products_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_route, prefix="/items")
app.include_router(users_route, prefix="/users")
app.include_router(products_route, prefix="/products")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
