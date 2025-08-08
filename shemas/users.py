from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field, validator
from typing import Optional

class UserCreate(BaseModel):
    """Check the sign up prompts"""
    email: EmailStr
    name: str
    password: str
class UserBase(BaseModel):
    """Users information with id"""
    email: EmailStr
    id: int
    name: str
class  TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"
    class Config:
        allow_population_by_field_name = True
    @validator("token")
    def hexlify_token(cls, value):
        """Converting UUID into the hex string"""
        return value.hex

class User(UserBase):
    """Create the body of the answer about details of user and its token"""
    token: TokenBase = {}
