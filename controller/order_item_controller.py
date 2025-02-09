from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from model.order_item import OrderItem
from model.order_item_remove import OrderItemRemove
from service import auth_service, order_item_service, order_service

router = APIRouter(
    prefix="/order_item",
    tags=["order_item"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create(order_item: OrderItem, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        await order_service.is_order_belong_to_user_id(user_info["id"], order_item.order_id)
        await order_item_service.create(order_item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(path="/", status_code=status.HTTP_200_OK)
async def delete_by_id(order_item_remove: OrderItemRemove, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        await order_service.is_order_belong_to_user_id(user_info["id"], order_item_remove.order_id)
        await order_item_service.delete_by_id(order_item_remove.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
