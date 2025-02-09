from typing import List


import requests

from config.config import Config
from model.order_response import OrderResponse

config = Config()


def get_all_orders(token: str) -> List[OrderResponse]:
    url = f"{config.BASE_URL}/order"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def add_item_to_order(order_item, token: str):
    url = f"{config.BASE_URL}/order_item"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=order_item)
    return response.json()


def remove_item_from_order(order_item_remove, token: str):
    url = f"{config.BASE_URL}/order_item"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers, json=order_item_remove)
    return response.json()


def delete_pending_order(order_id, token: str):
    url = f"{config.BASE_URL}/order/{order_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return response.json()


def create_pending_order(order_request, token: str):
    url = f"{config.BASE_URL}/order"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=order_request)
    return response.json()


def purchase_order(order_id: int, token: str):
    url = f"{config.BASE_URL}/order/purchase/{order_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers)
    return response.json()
