from typing import Optional

from passlib.context import CryptContext

from model import user_wrapper
from model.user import User
from model.user_request import UserRequest
from model.user_response import UserResponse
from repository import user_repository
from service import favorite_item_service, order_service

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


async def get_by_id(user_id: int) -> UserResponse:
    user = await user_repository.get_by_id(user_id)
    if user:
        return user_wrapper.user_to_user_response(user)
    else:
        raise Exception("user id does not exist")


async def is_username_unique(username: str) -> bool:
    user = await user_repository.get_by_username(username)
    if user is None:
        return True
    else:
        print(user)
        raise Exception("Username is already taken")


async def get_by_username(username: str) -> Optional[User]:
    user = await user_repository.get_by_username(username)
    if user:
        return user
    else:
        return None


async def create(user_request: UserRequest):
    await is_username_unique(user_request.username)
    user = user_wrapper.user_request_to_user(user_request)
    await user_repository.create(user)


async def soft_delete(user_id: int):
    await get_by_id(user_id)
    await favorite_item_service.delete_by_user_id(user_id)
    await order_service.delete_by_user_id(user_id)
    await user_repository.soft_delete(user_id)


def get_hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)
