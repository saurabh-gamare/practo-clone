from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, constr
from datetime import datetime


class CreateAppmtRequest(BaseModel):
    doctor_id: int 
    appmt_date: datetime    

    @field_validator("appmt_date")
    @classmethod
    def validate_appmt_date(cls, value: str): 
        if value < datetime.now():
            raise ValueError("Cannot make appointment in the past.")
        return value
    

class ListAppmtResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appmt_date: datetime
    created_at: datetime
    updated_at: datetime
    status: str

    class Config:
        from_attributes = True

    
    