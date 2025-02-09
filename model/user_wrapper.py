from model.user import User
from model.user_request import UserRequest
from model.user_response import UserResponse
from service import user_service


def user_request_to_user(user_request: UserRequest) -> User:
    user = User(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        phone=user_request.phone,
        address=user_request.address,
        username=user_request.username,
        hashed_password=user_service.get_hash_password(user_request.password),
        is_active=True
        )
    return user


def user_to_user_response(user: User) -> UserResponse:
    user_response = UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        address=user.address,
        username=user.username
        )
    return user_response
