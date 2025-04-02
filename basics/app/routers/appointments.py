from fastapi import APIRouter, Depends, Query
from starlette import status
from typing import Annotated, Literal

from database import db_dependency
from services.auth_service import CurrentUser
from services.appointments_service import CreateAppmtService, ListAppmtService
from schemas.appointments import CreateAppmtRequest, ListAppmtResponse


router = APIRouter(
    prefix='/appointments',
    tags=['appointments']
)

user_dependency = Annotated[dict, Depends(CurrentUser().get_current_user)]


@router.post("/create_appointment", 
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(CurrentUser().check_permission(["PATIENT"]))])
async def create_appointment_endpoint(db: db_dependency, request: CreateAppmtRequest, user: user_dependency):
    return await CreateAppmtService().create_appointment(db, request, user)


@router.get("/appointments", 
            response_model=list[ListAppmtResponse], 
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(CurrentUser().check_permission(["DOCTOR", "ADMIN"]))])
async def list_appointments_endpoint(db: db_dependency, user: user_dependency,
                                     status: Literal["PENDING", "COMPLETED", "CANCELLED", "RESCHEDULED"]=None, 
                                     offset: int=0, limit: int=10):
    return await ListAppmtService().list_appointments(db, offset, limit, status, user)





