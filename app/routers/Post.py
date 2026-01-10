from fastapi import APIRouter,Depends,status,HTTPException
from app.database.database import get_db
from sqlalchemy.orm import Session
from .Oauth2 import get_current_user
from app.models.Post import Posts
from app.limiter.limiter import limiter
from fastapi import Request,File,UploadFile,Form
from typing import List
from app.schemas.Post import Post_Response,Update_Post
import base64


router = APIRouter(
    prefix="/Posts",
    tags =['Posts']
)


@router.get("/user_post",response_model=List[Post_Response])
@limiter.limit("5/minute")
def get_all_posts(request:Request,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    posts = db.query(Posts).all()
    return posts


@router.get("/",response_model=List[Post_Response])
@limiter.limit("5/minute")
def get_user_post(request:Request,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    user_post = db.query(Posts).filter(Posts.owner_id == current_user.id).all()
    return user_post
    

@router.post("/",response_model=Post_Response)
async def create_user_post(text:str = Form(...),caption:str = Form(...),file:UploadFile = File(...),db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    if(file == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="file not found")
    data = await file.read()
    encode_file_data = base64.b64encode(data)
    new_post = Posts(text = text,caption = caption,owner_id = current_user.id,image = encode_file_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}",response_model=Post_Response)
def Update_post(id:int,update_post : Update_Post,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    post_update = db.query(Posts).filter(Posts.id == id)
    if post_update.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id {id}.")
    if post_update.first().id == current_user.id or current_user.role == "admin":
        post_update.update(update_post.dict(),synchronize_session=False)
        db.commit()
        return post_update.first()
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Denied.")

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    del_post = db.query(Posts).filter(Posts.id == id)
    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id {id}")
    if del_post.first().owner_id == current_user.id or current_user.role == "admin":
        del_post.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Denied.")
        
    



