from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from model.favorite_item import FavoriteItem
from model.favorite_item_response import FavoriteItemResponse
from service import auth_service, favorite_item_service

router = APIRouter(
    prefix="/favorite_item",
    tags=["favorite_item"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/", response_model=List[FavoriteItemResponse], status_code=status.HTTP_200_OK)
async def get_by_user_id(token: str = Depends(oauth2_bearer)) -> List[FavoriteItemResponse]:
    try:
        user_info = auth_service.validate_token(token)
        return await favorite_item_service.get_by_user_id(user_info['id'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(favorite_item: FavoriteItem, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        favorite_item.user_id = user_info['id']
        await favorite_item_service.create(favorite_item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(path="/{favorite_item_id}", status_code=status.HTTP_200_OK)
async def delete_by_id(favorite_item_id: int, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        await favorite_item_service.delete_by_id(user_info['id'], favorite_item_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
