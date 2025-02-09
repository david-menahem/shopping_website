from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from model.item import Item
from service import item_service

router = APIRouter(
    prefix="/item",
    tags=["item"]
)


@router.get(path="", response_model=List[Item], status_code=status.HTTP_200_OK)
async def get_all() -> List[Item]:
    try:
        return await item_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(path="/names", status_code=status.HTTP_200_OK)
async def get_by_names(names: List[str]) -> List[Item]:
    try:
        return await item_service.get_by_names(names)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(path="/price", status_code=status.HTTP_200_OK)
async def get_by_price(price: float, operator: str) -> List[Item]:
    try:
        return await item_service.get_by_price(price, operator)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(path="/stock", status_code=status.HTTP_200_OK)
async def get_by_stock(stock: int, operator: str) -> List[Item]:
    try:
        return await item_service.get_by_stock(stock, operator)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
