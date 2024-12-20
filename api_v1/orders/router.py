from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api_v1.orders.schemas import OrderOutSchema
from api_v1.orders.service import OrderService
from core.models.database import SessionDep
from core.models.models import Order, Product
from api_v1.products import crud

router = APIRouter()


@router.get("/", response_model=list[OrderOutSchema])
async def get_all_orders():
    return await OrderService.get_all()


@router.post("/", response_model=OrderOutSchema)
async def create_order(promocode: str):
    return await OrderService.create(promocode=promocode)


@router.post("/{order_id}/add_product/{product_id}")
async def add_product_to_order(session: SessionDep, order_id: int, product_id: int):
    product: Product = await crud.get_product(session=session, product_id=product_id)
    order = await session.get(Order, order_id, options=[selectinload(Order.products)])
    order.products.append(product)
    print(f"{order.products=}")
    await session.commit()
