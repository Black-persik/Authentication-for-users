
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException
from shemas import users
from utils import users as user_utils
from utils.dependecies import get_current_user

router = APIRouter()

@router.get("/sign-up", response_model=users.User)
async def create_user(user:users.UserCreate):
    db_user = await user_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detial="Email already registered")
    return await user_utils.create_user(user=user)
@router.post("auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_utils.get_user_by_email(email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user_utils.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return await user_utils.create_user_token(user_id=user['id'])

@router.get('/users/me', response_model=users.UserBase)
async def read_users_me(current_user: users.User = Depends(get_current_user)):
    return current_user