from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from model.AuthResponse import AuthResponse
from service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["tags"]
)


@router.post(path="/token", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> AuthResponse:
    try:
        user = await auth_service.authenticate_user(form_data.username, form_data.password)
        return auth_service.create_token(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
