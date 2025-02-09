from datetime import date
from typing import List

from model.enums.order_status import OrderStatus
from model.order_item_response import OrderItemResponse
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.orders import Orders
from repository import order_repository
from service import order_item_service, item_service, user_service


async def get_by_user_id(user_id: int) -> List[OrderResponse]:
    await user_service.get_by_id(user_id)
    order_response_list = []
    order_ids = await get_order_ids_by_user_id(user_id)
    for order_id in order_ids:
        order_response = await get_by_id(order_id)
        order_response_list.append(order_response)
    return order_response_list


async def get_order_ids_by_user_id(user_id: int) -> List[int]:
    order_ids = await order_repository.get_order_ids_by_user_id(user_id)
    ids = []
    for order_id in order_ids:
        ids.append(order_id[0])
    return ids


async def get_by_id(order_id: int) -> OrderResponse:
    order = await order_repository.get_by_id(order_id)
    if order:
        order_item_response_list = []
        order_items = await order_item_service.get_by_order_id(order_id)
        for order_item in order_items:
            item = await item_service.get_by_id(order_item.item_id)
            order_item_response = OrderItemResponse(id=order_item.id, item_name=item.name, price=item.price,
                                                    quantity=order_item.quantity)
            order_item_response_list.append(order_item_response)

        order_response = OrderResponse(
            id=order.id,
            user_id=order.user_id,
            order_date=order.order_date,
            shipping_address=order.shipping_address,
            status=order.status,
            items=order_item_response_list,
            total_price=calculate_total_price(order_item_response_list)
        )
        return order_response
    else:
        raise Exception("Order id does not exist")


async def check_pending_order_amount_by_user_id(user_id: int):
    count = await order_repository.check_pending_order_amount_by_user_id(user_id)
    if count > 0:
        raise Exception("User can have only one pending order")


async def is_order_belong_to_user_id(user_id: int, order_id: int):
    order_ids = await get_order_ids_by_user_id(user_id)
    if order_id not in order_ids:
        raise Exception("The order does not belong to the user")


async def create_pending(order_request: OrderRequest):
    await user_service.get_by_id(order_request.user_id)
    item = await item_service.get_by_id(order_request.order_item.item_id)
    item_service.is_in_stock(item.stock, order_request.order_item.quantity)
    order = Orders(user_id=order_request.user_id, order_date=date.today(),
                   shipping_address=order_request.shipping_address, status=OrderStatus.TEMP.value)
    await check_pending_order_amount_by_user_id(order_request.user_id)
    order_id = await order_repository.create_pending(order)
    order_request.order_item.order_id = order_id
    await order_item_service.create(order_request.order_item)


async def purchase(order_id: int):
    await is_order_purchased(order_id)
    order_items = await order_item_service.get_by_order_id(order_id)
    for order_item in order_items:
        await item_service.decrease_stock(order_item.item_id, order_item.quantity)
    await order_repository.purchase(order_id)


async def is_order_purchased(order_id: int):
    order = await order_repository.get_by_id(order_id)
    if order.status.value == OrderStatus.CLOSE.value:
        raise Exception("Order already purchased")


async def is_order_pending(order_id: int):
    order = await order_repository.get_by_id(order_id)
    if order.status.value != OrderStatus.TEMP.value:
        raise Exception("Order must be in pending status to be able to add items")


async def delete_pending_by_id(order_id: int):
    await order_repository.delete_by_id(order_id)


async def delete_by_user_id(user_id: int):
    order_ids = await get_order_ids_by_user_id(user_id)
    for order_id in order_ids:
        await order_item_service.delete_by_order_id(order_id)
    await order_repository.delete_by_user_id(user_id)


def calculate_total_price(order_item_response_list: List[OrderItemResponse]):
    total_price = 0
    for order_item_response in order_item_response_list:
        total_price += order_item_response.price*order_item_response.quantity
    return round(total_price, 2)
