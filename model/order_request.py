from typing import Optional

from pydantic import BaseModel

from model.order_item import OrderItem


class OrderRequest(BaseModel):
    user_id: Optional[int] = None
    shipping_address: str
    order_item: OrderItem

