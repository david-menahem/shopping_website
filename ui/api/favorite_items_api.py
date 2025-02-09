import requests

from config.config import Config

config = Config()


def get_favorite_items(token: str):
    url = f"{config.BASE_URL}/favorite_item/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def create_favorite_item(favorite_item, token: str):
    url = f"{config.BASE_URL}/favorite_item/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=favorite_item)
    return response.json()


def remove_favorite_item(favorite_item_id: int, token: str):
    url = f"{config.BASE_URL}/favorite_item/{favorite_item_id}"
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(url, headers=headers)
