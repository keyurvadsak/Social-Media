from app.database.database import Base
from sqlalchemy import Column, ForeignKey,Integer,TIMESTAMP



class Followers(Base):
    __tablename__ = "Followers"
    
    id = Column(Integer,autoincrement=True,primary_key=True)
    Following_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    Followers_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default="now()")