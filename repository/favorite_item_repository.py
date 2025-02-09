from typing import List

from model.favorite_item import FavoriteItem
from repository.database import database

TABLE = "favorite_item"


async def get_by_user_id(user_id: int) -> List[FavoriteItem]:
    query = f"SELECT * FROM {TABLE} WHERE user_id=:user_id"
    value = {"user_id": user_id}
    results = await database.fetch_all(query, value)
    return [FavoriteItem(**result) for result in results]


async def create(favorite_item: FavoriteItem):
    query = f"""
    INSERT INTO {TABLE}
    (user_id, item_id)
    VALUES 
    (:user_id, :item_id)
    """
    values = {"user_id": favorite_item.user_id, "item_id": favorite_item.item_id}
    await database.execute(query, values)


async def delete_by_id(favorite_item_id: int):
    query = f"DELETE FROM {TABLE} WHERE id=:favorite_item_id"
    value = {"favorite_item_id": favorite_item_id}
    await database.execute(query, value)


async def delete_by_user_id(user_id: int):
    query = f"DELETE FROM {TABLE} WHERE user_id=:user_id"
    value = {"user_id": user_id}
    await database.execute(query, value)


async def is_favorite_item_exist(user_id: int, item_id: int) -> bool:
    query = f"SELECT * FROM {TABLE} WHERE user_id=:user_id AND item_id=:item_id"
    values = {"user_id": user_id, "item_id": item_id}
    result = await database.fetch_one(query, values)
    if result:
        return True
    else:
        return False
