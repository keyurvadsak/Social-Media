from fastapi import APIRouter,Depends,HTTPException,status,Response
from .Oauth2 import get_current_user
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.User import UpdateProfile,UserProfileCheck
from app.utils.utils import verify_hashed_password,password_hashed


router = APIRouter(
    prefix="/Profile",
    tags=['Profile']    
)
@router.get("/Check",response_model=UserProfileCheck)
def get_user_info(db:Session=Depends(get_db),current_user = Depends(get_current_user)):
    user_info = db.query(User).filter(User.id == current_user.id).first()
    return user_info

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def Update_profile(id:int,user_update:UpdateProfile,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "User not found")
    if current_user.id != user.first().id and current_user.first().role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Denied.")
    if verify_hashed_password(user_update.old_password,user.first().password) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="old password are incorrect")
    
    update_data = {}
    
    update_data['name'] = user_update.name
    update_data['email'] = user_update.email
    update_data['password'] = password_hashed(user_update.new_password)
    user.update(update_data, synchronize_session=False)
    
    db.commit()
    return user.first()

@router.delete("/{id}")
def delete_user(id:int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id)
    print(user.first().role)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found.")
        
    if(user.first().id == current_user.id or current_user.role == "admin"):
        user.delete(synchronize_session=False)
        db.commit()
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Denied.")
        
    
    