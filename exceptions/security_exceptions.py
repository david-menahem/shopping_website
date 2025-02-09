from fastapi import HTTPException
from starlette import status


def create_token_exception() -> HTTPException:
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to create the token"
    )
    return exception


def token_exception() -> HTTPException:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The token provided is invalid"
    )
    return exception


def bad_credentials_exception() -> HTTPException:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email or password is incorrect"
    )
    return exception

