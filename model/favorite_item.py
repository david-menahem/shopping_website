from typing import Optional

from pydantic import BaseModel


class FavoriteItem(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    item_id: int
