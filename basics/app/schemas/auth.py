from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

from models.auth import Role



# Schemas are use for:
# 1. validating a request
# 2. return a response in the same format


class RegisterRequest(BaseModel):
    """
    ... is used for required field.
    """
    username: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    role: Role = Field(...)


    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):  
        if value == "testpassword":
            raise ValueError("Please use a different password.")
        return value
    
    @model_validator(mode="before")
    @classmethod
    def validate_request(cls, values: dict):
        """
        mode=before is used for Preprocessing data before type conversion.	
        dont use if you want to validate after type conversion. eg - Checking minimum length of a string.
        """
        if values.get("role"):
            print("Role -", values.get("role"))
        return values


class TokenResponse(BaseModel):
    access_token: str
    token_type: str