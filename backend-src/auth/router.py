from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import Token, User as UserSchema
from auth.auth import authenticate_user, auth_exception, get_current_user
from database.engine import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not Found"}, 401: {"description": "Invalid authentication"}}
)

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    token = await authenticate_user(form_data, db)
    if not token:
        raise auth_exception
    return token

@router.get("/me", response_model=UserSchema)
async def me(user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return user