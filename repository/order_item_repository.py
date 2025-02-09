from typing import List, Optional

from model.order_item import OrderItem
from repository.database import database

TABLE = "order_item"


async def get_by_order_id(order_id: int) -> List[OrderItem]:
    query = f"SELECT * FROM {TABLE} WHERE order_id=:order_id"
    value = {"order_id": order_id}
    results = await database.fetch_all(query, value)
    return [OrderItem(**result) for result in results]


async def get_by_id(order_item_id: int) -> Optional[OrderItem]:
    query = f"SELECT * FROM {TABLE} WHERE id=:order_item_id"
    values = {"order_item_id": order_item_id}
    result = await database.fetch_one(query, values)
    if result:
        return OrderItem(**result)
    else:
        return None


async def create(order_item: OrderItem):
    query = f"""
    INSERT INTO {TABLE}
    (order_id, item_id, quantity)
    VALUES 
    (:order_id, :item_id, :quantity)
    """
    values = {"order_id": order_item.order_id, "item_id": order_item.item_id, "quantity": order_item.quantity}
    await database.execute(query, values)


async def delete_by_id(order_item_id: int):
    query = f"DELETE FROM {TABLE} WHERE id=:order_item_id"
    value = {"order_item_id": order_item_id}
    await database.execute(query, value)


async def delete_by_order_id(order_id: int):
    query = f"DELETE FROM {TABLE} WHERE order_id=:order_id"
    value = {"order_id": order_id}
    await database.execute(query, value)
