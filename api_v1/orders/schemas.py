from pydantic import BaseModel


class OrderInSchema(BaseModel):
    promocode: str | None = None


class OrderOutSchema(BaseModel):
    id: int
    promocode: str | None = None
    # products: list[int]
