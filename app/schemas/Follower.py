from pydantic import BaseModel, conint

class Follower_add_remove (BaseModel):
    Follow_id :int
    dir : conint(le=1) # type: ignore