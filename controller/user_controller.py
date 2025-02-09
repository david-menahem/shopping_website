from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from model.user_request import UserRequest
from service import auth_service, user_service

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create(user_request: UserRequest):
    try:
        await user_service.create(user_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(path="/", status_code=status.HTTP_200_OK)
async def soft_delete(token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        await user_service.soft_delete(user_info["id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
