from pydantic import BaseModel

# Base User schema, missing the password for safety
class User(BaseModel):
    id: int
    username: str

# Corresponds to the User model in the database
class UserWithPW(User):
    password_hash: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
