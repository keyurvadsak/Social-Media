from fastapi import APIRouter,Depends,status,HTTPException
from app.schemas.Comment import Create_Comment,Update_Comment,DeleteComment
from app.database.database import get_db
from sqlalchemy.orm import Session
from .Oauth2 import get_current_user
from app.models.Post import Posts
from app.models.Comment import Comment
from sqlalchemy import func


router = APIRouter(
    prefix="/Comment",
    tags=['Comment']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def add_comment(comment_data:Create_Comment,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    Check_post = db.query(Posts).filter(Posts.id == comment_data.post_id).first()
    if Check_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    get_post_owner_id = db.query(Posts.owner_id).filter(Posts.id == comment_data.post_id).scalar()
    new_comment = Comment(**comment_data.dict(),user_id = current_user.id,post_owner_id = get_post_owner_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/UserComment")
def get_user_comment(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    user_comments = db.query(Comment).filter(Comment.user_id == current_user.id).all()
    print(user_comments)
    return user_comments


@router.get("/{id}")
def get_post_comments(id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    comments_of_post = db.query(Comment).filter(Comment.post_id == id).all()
    if comments_of_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Comments Found.")
    
    return comments_of_post



@router.put("/{id}")
def update_comment(id:int,update_comments : Update_Comment,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
        Check_post = db.query(Posts).filter(Posts.id == id).first()
        Check_comment = db.query(Comment).filter(Comment.post_id == id,Comment.user_id == current_user.id)
        if Check_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
        if Check_comment.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Comment not found.")
        print(Check_comment)
        # update_comment_data = Comment(update_comments.dict())
        Check_comment.update(update_comments.dict(),synchronize_session = False)
        db.commit()
        return Check_comment.first()
    

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
def delete_comment_by_admin(delete_comment : DeleteComment,db:Session =Depends(get_db),current_user = Depends(get_current_user)):
    if current_user.role == "admin":
        
        if delete_comment.user_id == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user_id is required for admin.")
        del_comment_get = db.query(Comment).filter(Comment.post_id == delete_comment.post_id,Comment.user_id == delete_comment.user_id)
    else:
        del_comment_get = db.query(Comment).filter(Comment.post_id == delete_comment.post_id,Comment.user_id == current_user.id)
        if del_comment_get.first().post_owner_id != current_user.id or del_comment_get.first().user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Denied.")
        
    if del_comment_get.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Comment not found')
    
    
    
    del_comment_get.delete(synchronize_session=False)
    db.commit()
    return {"data":"Comment Deleted."}

@router.get("/TotalComments/{id}")
def post_total_comment(id:int,db:Session = Depends(get_db),current_user=Depends(get_current_user)):
    total_comment = db.query(func.count(Comment.post_id).label("Post_Like")).filter(Comment.post_id == id).scalar()
    print (total_comment)
    return {"Total Comments":total_comment}
        
        
    
    

