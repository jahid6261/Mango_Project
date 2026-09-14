from pydantic import BaseModel,EmailStr,Field,ConfigDict
from typing import Optional
from src.users.models import UserRole 




class UserRegistrationRequest(BaseModel):

    first_name:str
    last_name:str
    email:str
    number:str
    password:str
    address:str
    
class UserLoginRequest(BaseModel):
    email:str
    password:str


class LoginResponse(BaseModel):
    access_token:str
    token_type:str='bearer'       


class UserProfileResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
    number:str
    address:str
    role:UserRole
    is_active: bool 
    model_config = ConfigDict(from_attributes=True)
        
        
class UpdateProfileRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    number: str | None = None
    address: str | None = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str  