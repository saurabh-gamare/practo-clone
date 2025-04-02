from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class ProfileRequest(BaseModel):
    profile_pic: str
    first_name: str
    last_name: str
    age: int = Field(ge=18)
    mobile: str = Field(max_length=10)
    email: EmailStr
    address: str
    speciality: str
    degree: str

