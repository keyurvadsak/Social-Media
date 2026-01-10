from pydantic import BaseModel
from datetime import datetime

class Update_Post(BaseModel):
    text:str
    caption:str
    
class Post_Response(BaseModel):
    id:int
    text:str
    caption:str
    created_at: datetime
    image:str
    
    class Config:
        orm_mode:True
    
    

    