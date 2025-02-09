from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    item_name: str
    price: float
    quantity: int
