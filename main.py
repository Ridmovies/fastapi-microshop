import uvicorn
from fastapi import FastAPI

from items_views import router as items_route
from users.views import router as users_route

app = FastAPI()
app.include_router(items_route, prefix="/items")
app.include_router(users_route, prefix="/users")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
