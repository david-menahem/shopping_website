from typing import Optional

from model.user import User
from repository.database import database

TABLE = "users"


async def get_by_id(user_id: int) -> Optional[User]:
    query = f"SELECT * FROM {TABLE} WHERE id=:user_id AND is_active=:is_active"
    values = {"user_id": user_id, "is_active": True}
    result = await database.fetch_one(query, values)
    if result:
        return User(**result)
    else:
        return None


async def get_by_username(username: str) -> Optional[User]:
    query = f"SELECT * FROM {TABLE} WHERE username=:username AND is_active=:is_active"
    values = {"username": username, "is_active": True}
    result = await database.fetch_one(query, values)
    if result:
        return User(**result)
    else:
        return None


async def create(new_user: User):
    query = f"""
    INSERT INTO {TABLE}
    (first_name, last_name, email, phone, address, 
    username, hashed_password, is_active)
    VALUES 
    (:first_name, :last_name, :email, :phone, :address, 
    :username, :hashed_password, :is_active)
    """
    values = {"first_name": new_user.first_name, "last_name": new_user.last_name,
              "email": new_user.email, "phone": new_user.phone, "username": new_user.username,
              "hashed_password": new_user.hashed_password, "address": new_user.address, "is_active": new_user.is_active}
    await database.execute(query, values)


async def soft_delete(user_id: int):
    query = f"""UPDATE {TABLE}
             SET is_active=:is_active
             WHERE id=:user_id
             """
    values = {"user_id": user_id, "is_active": False}
    await database.execute(query, values)
