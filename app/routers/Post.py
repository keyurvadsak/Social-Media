from fastapi import APIRouter,Depends,status,HTTPException
from app.database.database import get_db
from sqlalchemy.orm import Session
from .Oauth2 import get_current_user
from app.models.Post import Posts
from app.limiter.limiter import limiter
from fastapi import Request


router = APIRouter(
    prefix="/Posts",
    tags =['Posts']
)


@router.get("/")
@limiter.limit("5/minute")
def get_posts(request:Request,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    posts = db.query(Posts).all()
    return posts
    