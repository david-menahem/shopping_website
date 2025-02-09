from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from model.order_request import OrderRequest
from model.order_response import OrderResponse
from service import auth_service, order_service, user_service

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_by_user_id(token: str = Depends(oauth2_bearer)) -> List[OrderResponse]:
    try:
        user_info = auth_service.validate_token(token)
        return await order_service.get_by_user_id(user_info["id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=status.HTTP_200_OK)
async def create_pending(order_request: OrderRequest, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        order_request.user_id = user_info["id"]
        await order_service.create_pending(order_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/purchase/{order_id}", status_code=status.HTTP_200_OK)
async def purchase(order_id: int, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        await order_service.is_order_belong_to_user_id(user_info["id"], order_id)
        await order_service.purchase(order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_pending_order_by_id(order_id: int, token: str = Depends(oauth2_bearer)):
    try:
        user_info = auth_service.validate_token(token)
        await order_service.is_order_belong_to_user_id(user_info["id"], order_id)
        await order_service.delete_pending_by_id(order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
