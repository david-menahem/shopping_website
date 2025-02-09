from typing import List

from model.item import Item
from repository import item_repository
from repository.database import database


async def get_all() -> List[Item]:
    items = await item_repository.get_all()
    if items:
        return items
    else:
        return []


async def get_by_id(item_id: int) -> Item:
    existing_item = await item_repository.get_by_id(item_id)
    if existing_item:
        return existing_item
    else:
        raise Exception("Item id does not exist")


def is_in_stock(stock: int, amount: int) -> bool:
    if stock - amount >= 0:
        return True
    else:
        raise Exception("Insufficient stock amount requested")


async def decrease_stock(item_id: int, amount: int):
    async with database.transaction():
        item = await get_by_id(item_id)
        if is_in_stock(item.stock, amount):
            await item_repository.decrease_stock(item_id, amount)


async def get_by_names(names: List[str]) -> List[Item]:
    items_list = []
    for name in names:
        items = await item_repository.get_by_name(name)
        for item in items:
            if item not in items_list:
                items_list.append(item)
    return items_list


async def get_by_price(price: float, operator: str) -> List[Item]:
    check_operator_symbol(operator)
    return await item_repository.get_by_price(price, operator)


async def get_by_stock(stock: int, operator: str) -> List[Item]:
    check_operator_symbol(operator)
    return await item_repository.get_by_stock(stock, operator)


def check_operator_symbol(operator: str):
    valid_operators = ["<", "=", ">"]
    if operator not in valid_operators:
        raise Exception("Valid operator are '<', '=', '>'")
