from typing import List

from model.favorite_item import FavoriteItem
from model.favorite_item_response import FavoriteItemResponse
from repository import favorite_item_repository
from service import item_service, user_service


async def get_by_user_id(user_id: int) -> List[FavoriteItemResponse]:
    favorite_item_response_list = []
    await user_service.get_by_id(user_id)
    favorite_items = await favorite_item_repository.get_by_user_id(user_id)
    for favorite_item in favorite_items:
        item = await item_service.get_by_id(favorite_item.item_id)
        favorite_item_response = FavoriteItemResponse(
            id=favorite_item.id,
            user_id=favorite_item.user_id,
            item_name=item.name,
            stock=item.stock,
            price=item.price
        )
        favorite_item_response_list.append(favorite_item_response)
    return favorite_item_response_list


async def create(favorite_item: FavoriteItem):
    await is_favorite_item_exist(favorite_item.user_id, favorite_item.item_id)
    await favorite_item_repository.create(favorite_item)


async def delete_by_id(favorite_item_id: int):
    await favorite_item_repository.delete_by_id(favorite_item_id)


async def delete_by_user_id(user_id: int):
    await favorite_item_repository.delete_by_user_id(user_id)


async def is_favorite_item_exist(user_id: int, item_id: int):
    result = await favorite_item_repository.is_favorite_item_exist(user_id, item_id)
    if result:
        raise Exception("Duplicate favorite item cannot be added")
