from jose import JWTError,jwt
from datetime import datetime,timedelta
from app.config.config import settings
from app.schemas.Token import Token_data
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models.User import User
 
Oauth2_scene = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
        id = payload.get("user_id")
        if id == None:
            raise credential_exception
        token_data= Token_data(id = id)
        
        
    except JWTError:
        raise credential_exception    
    
    return token_data

def get_current_user(token:str = Depends(Oauth2_scene),db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"www-Authenticate":"Berear"})
    token = verify_access_token(token,credential_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
    