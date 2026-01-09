from app.database.database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text



class User(Base):
    __tablename__ = "Users"
    
    id= Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column (String,nullable=False)
    role = Column(String,nullable=False,server_default="user")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")
    