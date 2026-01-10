from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routers.Oauth2 import get_current_user
from app.schemas.Like import Likes
from app.models.Like import Like
from app.models.Post import Posts
from sqlalchemy import func

router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def add_del_like(like:Likes,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    post_like = db.query(Like).filter(Like.post_id == like.id,Like.user_id == current_user.id)
    found_like = post_like.first()
    found_post = db.query(Posts).filter(Posts.id == like.id).first()
    
    if like.dir == 1:
        if found_like == None:
            if found_post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found.")
            new_like = Like(post_id = like.id,user_id = current_user.id)
            db.add(new_like)
            db.commit()
            db.refresh(new_like)
            return new_like
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="post already liked")
    if like.dir == 0:
        if found_like == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post like not Found")
        post_like.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
@router.get("/{id}")
def get_post_like(id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    post_like = db.query(func.count(Like.user_id).label("Post_Like")).filter(Like.post_id == id).scalar()
    return {"Post_like":post_like}
    