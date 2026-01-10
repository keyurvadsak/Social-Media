from pydantic import BaseModel, conint

class Likes(BaseModel):
    id:int
    dir:conint(le=1) # type: ignore
    
