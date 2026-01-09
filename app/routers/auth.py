from fastapi import APIRouter,Depends,status,HTTPException
from app.schemas.User import UserCreate
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models.User import User
from app.utils.utils import password_hashed
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.utils import verify_hashed_password
from app.routers.Oauth2 import create_access_token

router = APIRouter(
    tags=['auth']
)


@router.post("/register",status_code=status.HTTP_201_CREATED)
def register_user(user:UserCreate,db:Session = Depends(get_db)):
    hash_password = password_hashed(user.password)
    user.password = hash_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user_info : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_info.username).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email not found")
    elif verify_hashed_password(user_info.password, user.password) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Password are Incorrect")
    
    access_token = create_access_token({"user_id": user.id})
    return {"access_token":access_token}
    
    
    
    