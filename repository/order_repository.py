from typing import List, Optional

from model.enums.order_status import OrderStatus
from model.orders import Orders
from repository.database import database

TABLE = "orders"


async def get_by_user_id(user_id) -> List[Orders]:
    query = f"SELECT * FROM {TABLE} WHERE user_id=:user_id"
    value = {"user_id": user_id}
    results = await database.fetch_all(query, value)
    return [Orders(**result) for result in results]


async def get_by_id(order_id) -> Optional[Orders]:
    query = f"SELECT * FROM {TABLE} WHERE id=:order_id"
    value = {"order_id": order_id}
    result = await database.fetch_one(query, value)
    if result:
        return Orders(**result)
    else:
        return None


async def get_order_ids_by_user_id(user_id: int) -> List[int]:
    query = f"SELECT id FROM {TABLE} WHERE user_id=:user_id"
    value = {"user_id": user_id}
    return await database.fetch_all(query, value)


async def create_pending(order: Orders) -> int:
    query = f"""
    INSERT INTO {TABLE}
    (user_id, order_date, shipping_address, status)
    VALUES 
    (:user_id, :order_date, :shipping_address, :status)
    """
    values = {"user_id": order.user_id, "order_date": order.order_date,
              "shipping_address": order.shipping_address, "status": order.status.value}
    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]


async def delete_by_user_id(user_id: int):
    query = f"DELETE FROM {TABLE} WHERE user_id=:user_id"
    value = {"user_id": user_id}
    await database.execute(query, value)


async def delete_by_id(order_id: int):
    query = f"DELETE FROM {TABLE} WHERE id=:order_id"
    value = {"order_id": order_id}
    await database.execute(query, value)


async def purchase(order_id: int):
    query = f"""UPDATE {TABLE}
             SET status=:status
             WHERE id=:order_id
             """
    values = {"order_id": order_id, "status": OrderStatus.CLOSE.value}
    await database.execute(query, values)


async def check_pending_order_amount_by_user_id(user_id: int) -> int:
    query = f"SELECT COUNT(*) FROM {TABLE} WHERE user_id=:user_id AND status=:status"
    values = {"user_id": user_id, "status": OrderStatus.TEMP.value}
    result = await database.fetch_one(query, values)
    if result[0] > 0:
        return result[0]
    else:
        return 0
