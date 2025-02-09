from typing import List

from model.order_item import OrderItem
from repository import order_item_repository
from service import item_service, order_service


async def get_by_order_id(order_id: int) -> List[OrderItem]:
    return await order_item_repository.get_by_order_id(order_id)


async def get_by_id(order_item_id: int) -> OrderItem:
    order_item = await order_item_repository.get_by_id(order_item_id)
    if order_item:
        return order_item
    else:
        raise Exception("The item does not exist in this order")


async def create(order_item: OrderItem):
    item = await item_service.get_by_id(order_item.item_id)
    item_service.is_in_stock(item.stock, order_item.quantity)
    await order_service.is_order_pending(order_item.order_id)
    await order_item_repository.create(order_item)


async def delete_by_id(order_item_id: int):
    await order_item_repository.delete_by_id(order_item_id)


async def delete_by_order_id(order_id: int):
    await order_item_repository.delete_by_order_id(order_id)

