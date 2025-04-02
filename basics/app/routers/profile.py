from fastapi import APIRouter, Depends
from starlette import status
from typing import Annotated

from database import db_dependency
from services.auth_service import CurrentUser
from services.profile_service import ProfileService
from schemas.profile import ProfileRequest


router = APIRouter(
    prefix='/profile',
    tags=['profile']
)

user_dependency = Annotated[dict, Depends(CurrentUser().get_current_user)]


@router.post("/create_profile", status_code=status.HTTP_201_CREATED)
async def get_profile_endpoint(db: db_dependency, request: ProfileRequest, user: user_dependency):
    return await ProfileService().create_profile(db, request, user)

@router.get("/analytics", status_code=status.HTTP_200_OK)
async def get_analytics_endpoint(db: db_dependency):
    pass
