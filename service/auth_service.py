from datetime import datetime, timezone, timedelta

from jose import jwt, JWTError

from config.config import Config
from exceptions import security_exceptions
from model.AuthResponse import AuthResponse
from model.user import User
from service import user_service

config = Config()


async def authenticate_user(username: str, password: str) -> User:
    user = await user_service.get_by_username(username)
    if user and user_service.verify_password(password, user.hashed_password):
        return user
    else:
        raise security_exceptions.bad_credentials_exception()


def validate_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload.get("id")
        username = payload.get("subject")
        if user_id and username:
            return {"id": user_id, "username": username}
        else:
            raise security_exceptions.token_exception()
    except JWTError:
        raise security_exceptions.token_exception()


def create_token(user: User) -> AuthResponse:
    try:
        token_expiry = datetime.now(timezone.utc) + timedelta(minutes=config.TOKEN_EXPIRY_TIME)
        user_date = {"subject": user.username, "id": user.id, "exp": token_expiry}
        jwt_token = jwt.encode(user_date, config.SECRET_KEY, config.ALGORITHM)
        return AuthResponse(jwt_token=jwt_token)
    except JWTError:
        raise security_exceptions.create_token_exception()
