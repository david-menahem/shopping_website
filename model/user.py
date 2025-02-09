from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    username: str
    hashed_password: str
    is_active: bool
