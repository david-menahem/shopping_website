from pydantic import BaseModel


class FavoriteItemResponse(BaseModel):
    id: int
    user_id: int
    item_name: str
    stock: int
    price: float
