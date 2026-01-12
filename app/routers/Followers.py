from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import func
from app.database.database import get_db
from app.models.Followers import Followers
from app.routers.Oauth2 import get_current_user
from app.schemas.Follower import Follower_add_remove
from sqlalchemy.orm import Session
from app.models.User import User

router = APIRouter(
    prefix="/Followers",
    tags=['Followers']
)


@router.post("/")
def add_remove_Follower(Follow_data:Follower_add_remove,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    Follow_user = db.query(Followers).filter(Followers.Following_id == Follow_data.Follow_id, Followers.Followers_id == current_user.id) 
    user_found = db.query(User).filter(User.id == Follow_data.Follow_id).first()
    Follow_user_found = Follow_user.first()
    
    if Follow_data.dir ==1:
        if Follow_user_found == None:
            if user_found == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
            add_Follow_User = Followers(Following_id = Follow_data.Follow_id,Followers_id = current_user.id)
            db.add(add_Follow_User)
            db.commit()
            db.refresh(add_Follow_User)
            return add_Follow_User
        
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Already Followed.")
    if Follow_data.dir == 0:
        if Follow_user_found == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Following not found.")
        if Follow_user.first().Followers_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")
        Follow_user.delete(synchronize_session=False)
        db.commit()
        
        

@router.get("/getFollwers/{id}")
def get_followers(id:int,db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    followers_count = db.query(func.count(Followers.Following_id)).filter(Followers.Following_id == id).scalar()
    return {"Followers":followers_count}

@router.get("/getFollowing/{id}")
def get_following(id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    followings = db.query(func.count(Followers.Followers_id)).filter(Followers.Followers_id == id).scalar()
    return {"Followings" : followings}
    