from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    
class UpdateProfile(BaseModel):
    name:str
    email:str
    old_password:str
    new_password:str
    
class UserProfileCheck(BaseModel):
    id:int
    name:str
    email:str
    created_at : datetime
    
    class Config:
        orm_mode:True
   
class UserOut(BaseModel):
    id:int
    name:str
    email:str
    created_at:datetime
    
    
    class Config:
        orm_mode:True
    

