from api_v1.services.base import BaseService
from core.models.models import Order


class OrderService(BaseService):
    model = Order
