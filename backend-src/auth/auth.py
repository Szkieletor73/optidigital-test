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

# Custom authentication exception, for simplicity when reusing.
auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication",
    headers={"WWW-Authenticate": "Bearer"},
)

hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Get user data. This doesn't include password - it's a "public-safe" function.
# We use next(get_db()) instead of pushing dependencies here to avoid having to pass
# the `db` param through several functions to get here.
async def get_user(username: str):
    db: Session = next(get_db())
    user: UserModel | None = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return UserSchema(id=user.id, username=user.username)
    return None

# Get user data, with the hashed password. This should only be used for authentication purposes.
# We use next(get_db()) instead of pushing dependencies here to avoid having to pass
# the `db` param through several functions to get here.
async def get_user_with_password(username: str):
    db: Session = next(get_db())
    user: UserModel | None = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return UserWithPW(id=user.id, username=user.username, password_hash=user.password_hash)
    return None

# Decodes the JWT token passed by the client, and tries to resolve it into a user.
# If user data is prevent and valid, then the user is considered authenticated with a valid token.
# Tokens can't really be spoofed because they'd need the correct secret to encode,
# so if the decoded data is correct, the token can be assumed valid.
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

# Helper function that returns a hashed version of the input string.
# We could just use hasher.hash directly, but this lets us reuse the same hasher in other modules.
def get_hash(password: str):
    return hasher.hash(password)

# Encodes token with given data and expiration parameters.
def encode_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded

# Entry point of the authentication flow. Takes OAuth2PasswordRequestForm data, verifies, and returns a token if login is valid.
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