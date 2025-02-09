from typing import Optional

from pydantic import BaseModel


class OrderItemRemove(BaseModel):
    id: int
    order_id: int
