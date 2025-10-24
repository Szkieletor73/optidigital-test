from datetime import timedelta, timezone
from datetime import datetime
import jwt
from typing import Annotated
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from database.engine import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.models import User as UserModel
from auth.schemas import Token, User as UserSchema, UserWithPW

# Hardcoded for demo purposes.
# Normally, we'd put these in environment variables and load via os.environ or dotenv
SECRET="fbd3e2407a1f3d9f094650fe0a85c52613367da0887d9d9ad5e1267562594f50"
ALGORITHM="HS256"
TOKEN_EXPIRE=60

auth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )
auth_exception1 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication1",
            headers={"WWW-Authenticate": "Bearer"},
        )
auth_exception2 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication2",
            headers={"WWW-Authenticate": "Bearer"},
        )

hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_user(username: str):
    db: Session = next(get_db())
    user: UserModel | None = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return UserSchema(id=user.id, username=user.username)
    return None

async def get_user_with_password(username: str):
    db: Session = next(get_db())
    user: UserModel | None = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return UserWithPW(id=user.id, username=user.username, password_hash=user.password_hash)
    return None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET, algorithms=ALGORITHM)
        if not payload.get("id") or not payload.get("username"):
            raise auth_exception
    except jwt.InvalidTokenError:
        raise auth_exception
    user: UserSchema | None = await get_user(payload.get("username"))
    if not user:
        raise auth_exception
    return user

def get_hash(password: str):
    return hasher.hash(password)

def encode_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded

async def authenticate_user(form_data: OAuth2PasswordRequestForm):
    user: UserWithPW | None = await get_user_with_password(form_data.username)
    if not user:
        raise auth_exception
    if not hasher.verify(form_data.password, user.password_hash):
        raise auth_exception
    
    token = encode_token(
        data = {
            "id": user.id,
            "username": user.username
        },
        expires_delta = timedelta(minutes=TOKEN_EXPIRE)
        )
    return Token(access_token=token)