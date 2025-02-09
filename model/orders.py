from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel

from model.enums.order_status import OrderStatus


class Orders(BaseModel):
    id: Optional[int] = None
    user_id: int
    order_date: Date
    shipping_address: str
    status: OrderStatus
