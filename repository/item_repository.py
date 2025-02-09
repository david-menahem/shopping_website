from typing import List, Optional

from model.item import Item
from repository.database import database

TABLE = "item"


async def get_all() -> List[Item]:
    query = f"SELECT * FROM {TABLE}"
    results = await database.fetch_all(query)
    return [Item(**result) for result in results]


async def get_by_id(item_id: int) -> Optional[Item]:
    query = f"SELECT * FROM {TABLE} WHERE id=:item_id"
    value = {"item_id": item_id}
    result = await database.fetch_one(query, value)
    if result:
        return Item(**result)
    else:
        return None


async def decrease_stock(item_id: int, amount: int):
    query = f"""
    UPDATE {TABLE}
    SET stock = stock -:amount
    WHERE id=:item_id
    """
    values = {"item_id": item_id, "amount": amount}
    await database.execute(query, values)


async def get_by_name(name: str) -> List[Item]:
    query = f"SELECT * FROM {TABLE} WHERE name LIKE :name"
    value = {"name": f"%{name}%"}
    results = await database.fetch_all(query, value)
    return [Item(**result) for result in results]


async def get_by_price(price: float, operator: str) -> List[Item]:
    if operator == "=":
        query = f"SELECT * FROM {TABLE} WHERE ABS(price-:price) < 0.0001"
    else:
        query = f"SELECT * FROM {TABLE} WHERE price{operator}:price"

    value = {"price": price}
    results = await database.fetch_all(query, value)
    return [Item(**result) for result in results]


async def get_by_stock(stock: int, operator: str) -> List[Item]:
    query = f"SELECT * FROM {TABLE} WHERE stock{operator}:stock"
    value = {"stock": stock}
    results = await database.fetch_all(query, value)
    return [Item(**result) for result in results]
