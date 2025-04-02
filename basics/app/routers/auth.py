from fastapi import APIRouter, Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from database import db_dependency
from schemas.auth import RegisterRequest, TokenResponse
from services.auth_service import CreateUser, Login


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(db: db_dependency, request: RegisterRequest):
    return await CreateUser().create_user(db, request)


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token_endpoint(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: db_dependency):
    return await Login().login(form_data, db)