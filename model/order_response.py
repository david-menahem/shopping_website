from sqlite3 import Date
from typing import List

from pydantic import BaseModel

from model.enums.order_status import OrderStatus
from model.order_item_response import OrderItemResponse


class OrderResponse(BaseModel):
    id: int
    user_id: int
    order_date: Date
    shipping_address: str
    status: OrderStatus
    items: List[OrderItemResponse]
    total_price: float
