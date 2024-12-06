from typing import Union

import uvicorn
from fastapi import FastAPI, Body
from pydantic import EmailStr, BaseModel

app = FastAPI()

class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/email/")
def send_email(user: CreateUser):
    return {"email": user.email}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)