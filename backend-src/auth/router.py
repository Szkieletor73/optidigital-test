from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import Token
from auth.auth import authenticate_user, auth_exception

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not Found"}, 401: {"description": "Invalid authentication"}}
)

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = await authenticate_user(form_data)
    if not token:
        raise auth_exception
    return token