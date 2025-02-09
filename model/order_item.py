from typing import Optional

from pydantic import BaseModel


class OrderItem(BaseModel):
    id: Optional[int] = None
    order_id: Optional[int] = None
    item_id: int
    quantity: int
