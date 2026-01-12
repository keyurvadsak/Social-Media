from typing import Optional
from pydantic import BaseModel
from fastapi import Depends
from app.routers.Oauth2 import get_current_user


class Create_Comment(BaseModel):
    post_id:int
    Comment_Text :str

class Update_Comment(BaseModel):
    Comment_Text:str
    
class DeleteComment(BaseModel):
        post_id :str
        user_id:Optional[str]
        