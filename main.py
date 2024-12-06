import uvicorn
from fastapi import FastAPI

from items_views import router as items_route


app = FastAPI()
app.include_router(items_route, prefix="/items")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
